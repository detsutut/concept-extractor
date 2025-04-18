import extract_cli
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--sslcert', action="store", dest='ssl_certfile', default=None)
parser.add_argument('--sslkey', action="store", dest='ssl_keyfile', default=None)

def extract(text:str, fuzzy_threshold:int, filter_tags_str:str, inclusion_flag:str, use_premium:bool)->pd.DataFrame:
    filter_tags = filter_tags_str.split(",")
    if len(filter_tags)==1:
        filter_tags=[]
    concepts_df = extract_cli.extract(text, fuzzy_threshold, filter_tags,
                                      exclude=inclusion_flag=="exclude", use_premium=use_premium)
    if concepts_df is None:
        return gr.DataFrame(pd.DataFrame(data= [[None,None,None,None]],
                                         columns=["id", "name", "match_score", "semantic_tags"]),
                            interactive=True)
    else:
        return gr.DataFrame(concepts_df,interactive=True)

def export_csv(d):
    d.to_csv("concepts.csv")
    return "concepts.csv"

import gradio as gr
import pandas as pd

with gr.Blocks() as demo:
    gr.Markdown("# SNOMED Concept Extractor")
    gr.Markdown("")
    with gr.Group():
        text_input = gr.Textbox(label="Text", lines=4)
        with gr.Accordion("Settings", open=False):
            filtered_tags_input = gr.Textbox(
                label="Filtered Tags",
                info="Each tag should be comma separated",
                placeholder="e.g. disease, procedure, body part",
                max_lines=1,
                scale=2,
            )
            filter_type_radio = gr.Radio(
                label="Filter Type",
                choices=["Inclusion", "Exclusion"],
                value="Inclusion",
                scale=1
            )
            min_overlap_slider = gr.Slider(minimum=0, maximum=100, value=100, label="Min overlap %", scale=2)
            premium_translation_radio = gr.Checkbox(
                label="Use Premium Translation",
                value=False,
                scale=1
            )
        submit_btn = gr.Button("Submit", variant="primary")
    with gr.Group():
        output_df = gr.DataFrame(pd.DataFrame([[None,None,None,None]],columns=["id", "name", "match_score", "semantic_tags"]), interactive=True)

        download_btn = gr.Button("Export CSV", variant='secondary')
        download_btn_hidden = gr.DownloadButton(visible=False, elem_id="download_btn_hidden")
        download_btn.click(fn=export_csv, inputs=output_df, outputs=[download_btn_hidden]).then(fn=None, inputs=None,
                                                                                                  outputs=None,
                                                                                                  js="() => document.querySelector('#download_btn_hidden').click()")
    # Event binding
    submit_btn.click(
        fn=extract,
        inputs=[text_input, min_overlap_slider, filtered_tags_input, filter_type_radio, premium_translation_radio],
        outputs=output_df
    )

demo.queue(max_size=20)
demo.launch(server_name="0.0.0.0", server_port=7878, 
            ssl_keyfile = args.ssl_keyfile, 
            ssl_certfile = args.ssl_certfile,
            ssl_verify=False, pwa=True)
