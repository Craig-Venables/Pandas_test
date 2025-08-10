import sys
import threading
import configparser

from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QSpinBox,
    QTextEdit,
    QMessageBox,
)

# App logic imports
import file as f
import memristors.analysis as mem
import memristors.statistics_mem as stat_mem
import memristors.analysis_curated as curr
import memristors.print_mem as p
import memristors.currat_data as m
from memristors.report import generate_preview_report
import pickle
import os


class RunnerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    log = pyqtSignal(str)


class AnalysisRunner:
    def __init__(self, params: dict, environment: str, signals: RunnerSignals):
        self.params = params
        self.environment = environment
        self.signals = signals

    def _log(self, message: str) -> None:
        self.signals.log.emit(message + "\n")

    def run(self) -> None:
        try:
            # Load config
            config = configparser.ConfigParser()
            config.read('config.ini')

            excel_path = config[self.environment]['excel_path']
            main_dir = config[self.environment]['main_dir']
            curr_data_path = config[self.environment].get('curr_data_path', '')

            # Redirect stdout to file + console
            output_file_path = os.path.join(main_dir, 'printlog.txt')
            os.makedirs(main_dir, exist_ok=True)
            output_file = open(output_file_path, 'w', encoding='utf-8')
            original_stdout = sys.stdout
            sys.stdout = f.Tee(file=output_file, stdout=original_stdout)

            try:
                # Display options
                mem.set_pandas_display_options()

                memristors_data = self.params.get('memristors_data', True)
                currated = self.params.get('currated', False)

                # Run analysis
                if memristors_data:
                    self._log("Starting analysis (memristors_data=True)")
                    material_stats_dict, material_sweeps_dict, material_data, file_info_dict = mem.memristor_devices(
                        main_dir, self.params, excel_path
                    )
                else:
                    self._log("memristors_data=False, loading previously generated pickles if available...")
                    # Load previously generated dictionaries
                    try:
                        with open(os.path.join(main_dir, 'material_stats_dict_all.pkl'), 'rb') as file:
                            material_stats_dict = pickle.load(file)
                        with open(os.path.join(main_dir, 'material_sweeps_dict_all.pkl'), 'rb') as file:
                            material_sweeps_dict = pickle.load(file)
                        with open(os.path.join(main_dir, 'material_data_all.pkl'), 'rb') as file:
                            material_data = pickle.load(file)
                        with open(os.path.join(main_dir, 'file_info_dict.pkl'), 'rb') as file:
                            file_info_dict = pickle.load(file)
                    except FileNotFoundError as e:
                        raise RuntimeError(f"Required pickle not found when memristors_data=False: {e}")

                # Optional operations
                if self.params.get('sort_graphs', False):
                    self._log("Sorting graphs and copying data...")
                    m.data_copy(material_data, main_dir)

                if currated and curr_data_path:
                    self._log("Processing curated data...")
                    curr.currated_data(curr_data_path)

                # Stats and printing
                self._log("Calculating yields and rankings...")
                p.yield_calc(material_sweeps_dict)
                sample_sweeps = stat_mem.get_num_sweeps_ordered(file_info_dict, material_sweeps_dict)
                p.top_10_measured(sample_sweeps)

                on_off_ratio_info = mem.Files_.process_property(material_stats_dict, 'ON_OFF_Ratio')
                normalised_area_info = mem.Files_.process_property(material_stats_dict, 'normalised_area')
                p.print_on_off_ratio_info(on_off_ratio_info)
                p.print_normalised_area_info(normalised_area_info)

                on_off_ratio_info_list, top_samples_with_rep_on, top_samples_without_rep_on = stat_mem.find_top_samples(
                    material_stats_dict, property_name='ON_OFF_Ratio'
                )
                normalized_area_info_list, top_samples_with_rep_norm, top_samples_without_rep_norm = stat_mem.find_top_samples(
                    material_stats_dict, property_name='normalised_area'
                )

                print("Top Samples (With Repetition) - ON-OFF Ratio:")
                for idx, sample_info in enumerate(on_off_ratio_info_list[:10], start=1):
                    print(
                        f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, ON-OFF Ratio: {sample_info['property_value']}"
                    )

                print("\nTop Samples (Without Repetition) - ON-OFF Ratio:")
                for idx, sample_key in enumerate(top_samples_without_rep_on[:10], start=1):
                    sample_info = next(info for info in on_off_ratio_info_list if info['sample_key'] == sample_key)
                    print(
                        f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, ON-OFF Ratio: {sample_info['property_value']}"
                    )

                print("\nTop Samples (With Repetition) - Normalized Area:")
                for idx, sample_info in enumerate(normalized_area_info_list[:10], start=1):
                    print(
                        f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, Normalized Area: {sample_info['property_value']}"
                    )

                print("\nTop Samples (Without Repetition) - Normalized Area:")
                for idx, sample_key in enumerate(top_samples_without_rep_norm[:10], start=1):
                    sample_info = next(info for info in normalized_area_info_list if info['sample_key'] == sample_key)
                    print(
                        f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, Normalized Area: {sample_info['property_value']}"
                    )

                self._log("Analysis complete. See printlog.txt for details.")
            finally:
                # Restore stdout
                try:
                    sys.stdout.flush()
                except Exception:
                    pass
                sys.stdout = original_stdout
                try:
                    output_file.flush()
                    output_file.close()
                except Exception:
                    pass

            self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memristor Analysis Runner")

        self.env_combo = QComboBox()
        self.env_combo.addItems(["HOME_PC", "LAPTOP", "NOTTS_PC"])
        self.env_combo.setToolTip("Select the environment section from config.ini to use for paths")

        # Parameter checkboxes
        self.memristors_cb = QCheckBox("Analyse memristors data")
        self.memristors_cb.setChecked(True)
        self.memristors_cb.setToolTip("Run analysis across data folders and generate statistics and plots")

        self.currated_cb = QCheckBox("Analyse curated data")
        self.currated_cb.setToolTip("Process curated data in the configured curated data path")

        self.plot_graph_cb = QCheckBox("Plot graphs")
        self.plot_graph_cb.setChecked(True)
        self.plot_graph_cb.setToolTip("Generate and save per-file and combined plots")

        self.plot_gif_cb = QCheckBox("Create GIFs")
        self.plot_gif_cb.setToolTip("Create GIFs for devices with multiple sweeps")

        self.sort_graphs_cb = QCheckBox("Sort graphs")
        self.sort_graphs_cb.setToolTip("Copy/sort graphs into convenient folders")

        self.origin_graphs_cb = QCheckBox("Plot in Origin")
        self.origin_graphs_cb.setToolTip("Export data and plots to Origin for further use")

        self.pull_fabrication_cb = QCheckBox("Pull fabrication info from Excel")
        self.pull_fabrication_cb.setToolTip("Read fabrication info from the solutions/devices Excel file")

        self.save_df_cb = QCheckBox("Save DataFrames to CSV")
        self.save_df_cb.setToolTip("Save processed DataFrames to CSV alongside device folders")

        self.re_save_graph_cb = QCheckBox("Overwrite existing plots")
        self.re_save_graph_cb.setToolTip("If enabled, regenerate plots even if they already exist")

        self.re_analyse_cb = QCheckBox("Re-analyse existing results")
        self.re_analyse_cb.setToolTip("Force re-analysis even if outputs exist (reserved for future use)")

        self.skip_half_cb = QCheckBox("Skip half-sweeps")
        self.skip_half_cb.setToolTip("If a sweep is detected as half-sweep, skip it entirely")

        self.save_parquet_cb = QCheckBox("Also save Parquet")
        self.save_parquet_cb.setToolTip("Save a Parquet copy of per-file DataFrames (faster/smaller)")

        self.preview_report_cb = QCheckBox("Generate preview HTML report")
        self.preview_report_cb.setToolTip("Create a small HTML report of top-10 ON_OFF and Normalized Area")

        # Parallel workers control
        self.workers_spin = QSpinBox()
        self.workers_spin.setMinimum(1)
        try:
            import os as _os
            max_cpus = max(1, (_os.cpu_count() or 4))
        except Exception:
            max_cpus = 4
        self.workers_spin.setMaximum(max_cpus)
        # Sensible default without overwhelming system
        self.workers_spin.setValue(min(4, max_cpus))

        # Run controls
        self.run_button = QPushButton("Run Analysis")
        self.run_button.clicked.connect(self.on_run)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)

        # Layout
        root = QWidget()
        grid = QGridLayout()
        row = 0

        grid.addWidget(QLabel("Environment"), row, 0)
        grid.addWidget(self.env_combo, row, 1)
        row += 1

        grid.addWidget(self.memristors_cb, row, 0, 1, 2)
        row += 1
        grid.addWidget(self.currated_cb, row, 0, 1, 2)
        row += 1

        grid.addWidget(self.plot_graph_cb, row, 0)
        grid.addWidget(self.plot_gif_cb, row, 1)
        row += 1
        grid.addWidget(self.sort_graphs_cb, row, 0)
        grid.addWidget(self.origin_graphs_cb, row, 1)
        row += 1
        grid.addWidget(self.pull_fabrication_cb, row, 0)
        grid.addWidget(self.save_df_cb, row, 1)
        row += 1
        grid.addWidget(self.re_save_graph_cb, row, 0)
        grid.addWidget(self.re_analyse_cb, row, 1)
        row += 1

        grid.addWidget(self.skip_half_cb, row, 0)
        grid.addWidget(self.save_parquet_cb, row, 1)
        row += 1

        grid.addWidget(QLabel("Parallel workers"), row, 0)
        grid.addWidget(self.workers_spin, row, 1)
        row += 1

        grid.addWidget(self.preview_report_cb, row, 0)
        row += 1

        grid.addWidget(self.run_button, row, 0, 1, 2)
        row += 1

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(QLabel("Log:"))
        vbox.addWidget(self.log_view, 1)

        root.setLayout(vbox)
        self.setCentralWidget(root)
        self.resize(700, 600)

    def append_log(self, text: str) -> None:
        self.log_view.moveCursor(QTextCursor.MoveOperation.End)
        self.log_view.insertPlainText(text)
        self.log_view.moveCursor(QTextCursor.MoveOperation.End)

    def on_run(self):
        self.run_button.setEnabled(False)
        self.log_view.clear()
        self.append_log("Starting...\n")

        params = f.create_params_dict(
            plot_graph=self.plot_graph_cb.isChecked(),
            plot_gif=self.plot_gif_cb.isChecked(),
            sort_graphs=self.sort_graphs_cb.isChecked(),
            origin_graphs=self.origin_graphs_cb.isChecked(),
            pull_fabrication_info_excell=self.pull_fabrication_cb.isChecked(),
            save_df=self.save_df_cb.isChecked(),
            re_save_graph=self.re_save_graph_cb.isChecked(),
            re_analyse=self.re_analyse_cb.isChecked(),
            skip_half_sweeps=self.skip_half_cb.isChecked(),
            parallel_workers=self.workers_spin.value(),
            save_parquet=self.save_parquet_cb.isChecked(),
        )
        # include top-level flags used in main
        params['memristors_data'] = self.memristors_cb.isChecked()
        params['currated'] = self.currated_cb.isChecked()

        env = self.env_combo.currentText()

        self.signals = RunnerSignals()
        self.signals.log.connect(self.append_log)
        self.signals.finished.connect(self.on_finished)
        self.signals.error.connect(self.on_error)

        runner = AnalysisRunner(params=params, environment=env, signals=self.signals)

        # Run in background thread to keep UI responsive
        thread = threading.Thread(target=runner.run, daemon=True)
        thread.start()

    def on_finished(self):
        self.append_log("Done.\n")
        self.run_button.setEnabled(True)
        # Optionally generate preview report
        try:
            if self.preview_report_cb.isChecked():
                # Try to reload stats from last run
                config = configparser.ConfigParser()
                config.read('config.ini')
                main_dir = config[self.env_combo.currentText()]['main_dir']
                with open(os.path.join(main_dir, 'material_stats_dict_all.pkl'), 'rb') as fstats:
                    material_stats_dict = pickle.load(fstats)
                # Use the same property extraction utilities
                on_off_ratio_info_list, *_ = stat_mem.find_top_samples(material_stats_dict, property_name='ON_OFF_Ratio')
                normalized_area_info_list, *_ = stat_mem.find_top_samples(material_stats_dict, property_name='normalised_area')
                report_path = generate_preview_report(main_dir, on_off_ratio_info_list, normalized_area_info_list)
                self.append_log(f"Preview report: {report_path}\n")
        except Exception as e:
            self.append_log(f"Report generation failed: {e}\n")
        QMessageBox.information(self, "Completed", "Analysis finished. See printlog.txt in the configured main_dir.")

    def on_error(self, message: str):
        self.append_log(f"Error: {message}\n")
        self.run_button.setEnabled(True)
        QMessageBox.critical(self, "Error", message)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()