import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

save_folder = "images"

def basicPlot(df, save_name, show = False):
    fig = px.scatter(df, x="num_appearance", y="download_count", text="tag", color="tag")
    fig.update_traces(marker={'size': 15}, textposition='top center', hovertemplate="%{text}<extra></extra>")
    fig.update_layout(title_text="Popular {}".format(save_name))

    fig.write_image("images/{}.png".format(save_name))
    if show:
        fig.show()

def plotCategory(df, show = False):
    if df = None:
        df = pd.read_csv("hentai_data.csv")
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    category_counts = category_counts[category_counts['Count'] >= 1]
    fig = px.bar(category_counts, x='Category', y='Count', title='Category Counts')
    fig.write_image("images/category_plot.png")
    if show:
        fig.show()

def plotOverall():
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    df = pd.read_csv("hentai_data_tag.csv")

    overall = df.head(20)
    basicPlot(overall, "overall")

    character = df.loc[df['category'] == 'character'][:20]
    basicPlot(character, "character")

    parody = df.loc[df['category'] == 'parody'][:20]
    basicPlot(parody, "parody")

    df_data = pd.read_csv("hentai_data.csv")
    plotCategory(df_data)


if __name__ == '__main__':
    plotOverall()   
    plotCategory()
    
