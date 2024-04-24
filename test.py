import pickle

#for removing single item
# def remove_entry_from_pickle(pickle_file, key_to_remove):
#     # Load the pickle file
#     with open(pickle_file, 'rb') as f:
#         data = pickle.load(f)
#
#     # Remove the entry with the specified key
#     if key_to_remove in data:
#         del data[key_to_remove]
#         print(f"Entry with key '{key_to_remove}' removed.")
#     else:
#         print(f"No entry found with key '{key_to_remove}'.")
#
#     # Save the modified data back to the pickle file
#     with open(pickle_file, 'wb') as f:
#         pickle.dump(data, f)
#         print("Pickle file updated.")
#
# # Example usage:
# pickle_file = 'checked_files.pkl'
# key_to_remove = "Quantum Dots - Zn-Cu-In-S(Zns) - D33-0.07mgml-Gold-PS(2%)-Gold-s4 - G - 7 - 3-fs-1.0v-0.05sv-100ua.txt"
# remove_entry_from_pickle(pickle_file, key_to_remove)



def remove_entries_containing_substring(pickle_file, substring_to_remove):
    # Load the pickle file
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)

    # Remove entries containing the specified substring in their keys
    removed_entries = 0
    keys_to_remove = [key for key in data.keys() if substring_to_remove in key]
    for key in keys_to_remove:
        del data[key]
        removed_entries += 1

    if removed_entries > 0:
        print(f"Removed {removed_entries} entries containing the substring '{substring_to_remove}'.")
    else:
        print(f"No entries found containing the substring '{substring_to_remove}'.")

    # Save the modified data back to the pickle file
    with open(pickle_file, 'wb') as f:
        pickle.dump(data, f)
        print("Pickle file updated.")

# Example usage:
pickle_file = 'checked_files.pkl'
substring_to_remove = "D35-0.4mgml-Gold-PS(2%)-Gold-s6"
remove_entries_containing_substring(pickle_file, substring_to_remove)
# with open(pickle_file, 'rb') as f:
#     data = pickle.load(f)
#     print(data)