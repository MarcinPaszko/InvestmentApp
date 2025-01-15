import black
import sys

def format_js(file_path, output_file):
    try:
        # Read the JavaScript file
        with open(file_path, "r") as file:
            content = file.read()

        # Format the content using black with JavaScript options
        mode = black.Mode(
            target_versions={black.TargetVersion.ES2020},
            line_length=80,
            is_pyi=False,
            string_normalization=True,
            experimental_string_processing=True,
        )
        formatted_code = black.format_str(content, mode=mode)

        # Write the formatted code to the output file
        with open(output_file, "w") as output:
            output.write(formatted_code)

        print(f"Formatted code saved to {output_file}")

    except Exception as e:
        print(f"Error formatting file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python format_js_map.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    format_js(input_file, output_file)
