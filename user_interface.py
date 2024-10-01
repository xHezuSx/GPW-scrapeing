import gradio as gr
from scrape_script import scrape

with gr.Blocks(title="GPW Scraping tool") as demo:
    """INTERFACE"""
    with gr.Row():
        with gr.Column():
            company_name = gr.Textbox(
                label="Company Name",
                info="What company report you would like to check?"
            )
            report_amount = gr.Slider(
                1, 150, label="Report amount",
                info="How many reports would you like to take?",
                value=20, step=1
            )
            with gr.Column():
                download_checkbox = gr.Checkbox(
                    value=True,
                    interactive=True,
                    label="Download the CSV report?",
                )
            with gr.Column():
                download_types_file = gr.Checkboxgroup(['PDF', 'HTML'],
                                                       label="Downloa",
                                                       info="Some reports files may be heavy so downloading may take a while")
        with gr.Column():
            date = gr.Textbox(
                label="Date (optional)",
                info="From which day you would like to check reports? (dd-mm-yyyy). If empty all dates will be taken.",
                max_length=10
            )
            report_types = gr.Checkboxgroup(
                ['current', 'semi-annual', 'quarterly', 'interim', 'annual'],
                label="Report type",
                info="What type of report would you like to take?",
                value=['current', 'semi-annual', 'quarterly', 'interim', 'annual']
            )
            categories = gr.Checkboxgroup(
                ['EBI', 'ESPI'],
                label="Report category",
                info="What category of report would you like to take?",
                value=['EBI', "ESPI"]
            )

            output_text = gr.Textbox(label="Output")
    output_dataframe = gr.DataFrame(
        headers=['date', 'title', 'report type', 'report category', 'exchange rate', 'rate change', 'link'],
        label="Scraped data"
    )
    submit_btn = gr.Button("Submit")

    # Związanie funkcji z interfejsem
    submit_btn.click(
        fn=scrape,
        inputs=[company_name, report_amount, date, report_types, categories, download_checkbox, download_types_file],
        outputs=[output_text, output_dataframe])

demo.launch()
