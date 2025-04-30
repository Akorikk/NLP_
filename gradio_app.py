import gradio as gr

def get

def main():
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Classification (Zero short Classifiers)</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()  
                    with gr.Column():
                        them_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label= "subtitles or script Path")
                        save_path = gr.Textbox(label="Save Path")
                        get_theme_button = gr.Button("Get Themes")
                        et_theme_button.click(get_themes, inputs=[theme_list,subtitles_path,save_path])

    iface.launch(share=True)                   


if __name__ == "__main__":
    main()    