from tkinter.filedialog import askdirectory

def userOptionsMenu():
        options_for_input_media_type = ["image", "video"]
        options_for_input_media_color = ["grayscale", "color"]
        
        prompt_for_input_media_type = "Please select from the following: " + " ".join(options_for_input_media_type) + "\n"
        prompt_for_input_media_color = "Please select from the following: " + " ".join(options_for_input_media_color) + "\n"

        try:
            selected_input_media_type = input(
                prompt_for_input_media_type
            ).strip().lower()
            selected_input_media_color = input(
                prompt_for_input_media_color
            ).strip().lower()
            max_number_of_processes = int(input(
                "Maximum number of processes:"
            ).strip())
            input_data_abs_path = askdirectory(
                title='Select Input Folder'
            )
            output_data_abs_path = askdirectory(
                title='Select Output Folder'
            )
        except:
            raise

        def checkMenuOptions():
            if (
                selected_input_media_type in options_for_input_media_type and 
                selected_input_media_color in options_for_input_media_color
            ):
                return
            else:
                raise ValueError("Options does not match.")

        checkMenuOptions()

        return (
            selected_input_media_type, 
            selected_input_media_color, 
            input_data_abs_path, 
            output_data_abs_path,
            max_number_of_processes
        )