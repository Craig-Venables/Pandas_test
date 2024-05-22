""" old code to attempt to characterise a txt file and the type of data it was ie capsacative memristive etc - dosnt work"""

cross_points = categorize_device(df['voltage'], df["current"])

def categorize_device(voltage_data, current_data):
    def find_crossings(voltage_data: np.ndarray, current_data: np.ndarray):
        """
        Find the points of intersection between a voltage and current trace.
        Returns:
            List[Tuple[float, float]]: A list of tuples containing the intersection points.
        """
        voltage_data = voltage_data.to_numpy()
        current_data = current_data.to_numpy()

        crossings = []
        tolerance = 0.1

        # Ensure both voltage and current data have the same length
        if len(voltage_data) != len(current_data):
            raise ValueError("Voltage and current data must have the same length.")

        # Iterate through the data to find crossings
        for i in range(1, len(voltage_data)):
            if (
                    (voltage_data[i - 1] < current_data[i - 1] and voltage_data[i] > current_data[i])
                    or (voltage_data[i - 1] > current_data[i - 1] and voltage_data[i] < current_data[i])
            ) and abs(voltage_data[i] - current_data[i]) <= tolerance:
                crossing_point = (voltage_data[i], current_data[i])
                crossings.append(crossing_point)

        return crossings

    crossings = find_crossings(voltage_data, current_data)

    if not crossings:
        return "Capacitive", False

    # Check for one or two crossings for memristive behavior
    if 1 <= len(crossings) <= 2:
        # Check if the crossings are close to (0, 0)
        for point in crossings:
            if abs(point[0]) <= 0.1 and abs(point[1]) <= 0.1:
                return "Memristive", True

    # Check for more than 4 crossings for capacitive behavior
    elif len(crossings) > 4:
        return "Capacitive", True

    # If there are crossings but none near (0, 0), it's likely ohmic
    return "Ohmic", True