import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def visualize_from_llm_response(df, query, llm_response):
    try:
        chart_type = llm_response.get("chart_type")
        group_by = llm_response.get("group_by", [])

        if chart_type == "correlation_heatmap":
            corr = df.select_dtypes(include='number').corr()
            fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
            return fig

        if not group_by or not isinstance(group_by, list) or group_by[0] not in df.columns:
            return None

        x = group_by[0]
        y = group_by[1] if len(group_by) > 1 and group_by[1] in df.columns else None

        if chart_type == "bar":
            return px.bar(df, x=x, y=y)
        elif chart_type == "line":
            return px.line(df, x=x, y=y)
        elif chart_type == "scatter":
            return px.scatter(df, x=x, y=y)
        elif chart_type == "box":
            return px.box(df, x=x, y=y)
        elif chart_type == "histogram":
            return px.histogram(df, x=x)
        elif chart_type == "pie" and x:
            return px.pie(df, names=x, values=y if y else None)
        elif chart_type == "violin" and y:
            return px.violin(df, x=x, y=y, box=True, points="all")
        elif chart_type == "area" and y:
            return px.area(df, x=x, y=y)
        else:
            return None

    except Exception as e:
        print(f"Visualization error: {e}")
        return None


def visualize_comparison_side_by_side(df1, df2, x, y, chart_type="bar"):
    try:
        fig1, fig2 = None, None
        if chart_type == "bar":
            fig1 = px.bar(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.bar(df2, x=x, y=y, title="Dataset 2")
        elif chart_type == "line":
            fig1 = px.line(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.line(df2, x=x, y=y, title="Dataset 2")
        elif chart_type == "scatter":
            fig1 = px.scatter(df1, x=x, y=y, title="Dataset 1")
            fig2 = px.scatter(df2, x=x, y=y, title="Dataset 2")
        return fig1, fig2
    except Exception as e:
        return None, None

def visualize_comparison_overlay(df1, df2, x, y, label1="Dataset 1", label2="Dataset 2", chart_type="line"):
    try:
        fig = go.Figure()
        explanation = f"### Comparison Summary\n- **X-Axis:** {x}\n- **Y-Axis:** {y}\n\n"

        if chart_type == "line":
            fig.add_trace(go.Scatter(x=df1[x], y=df1[y], mode='lines+markers', name=label1))
            fig.add_trace(go.Scatter(x=df2[x], y=df2[y], mode='lines+markers', name=label2))
            explanation += "- A line chart helps visualize trends and differences over time or ordered categories.\n"
        elif chart_type == "bar":
            fig.add_trace(go.Bar(x=df1[x], y=df1[y], name=label1))
            fig.add_trace(go.Bar(x=df2[x], y=df2[y], name=label2))
            explanation += "- Bar charts are ideal for visualizing absolute differences between categories like `track_id` and `streams`.\n"
        elif chart_type == "scatter":
            fig.add_trace(go.Scatter(x=df1[x], y=df1[y], mode='markers', name=label1))
            fig.add_trace(go.Scatter(x=df2[x], y=df2[y], mode='markers', name=label2))
            explanation += "- Scatter plots show correlation and distribution between two numeric fields across datasets.\n"

        fig.update_layout(title=f"Overlay Comparison of {y} by {x}", barmode="group")
        return fig, explanation
    except Exception as e:
        return None, "Error generating explanation."

def render_chart(df, chart_type, x, y=None):
    if chart_type == "bar":
        return px.bar(df, x=x, y=y)
    elif chart_type == "line":
        return px.line(df, x=x, y=y)
    elif chart_type == "scatter":
        return px.scatter(df, x=x, y=y)
    elif chart_type == "histogram":
        return px.histogram(df, x=x)
    elif chart_type == "pie":
        return px.pie(df, names=x, values=y) if y else px.pie(df, names=x)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")
