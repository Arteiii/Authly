use axum::response::Html;

pub(crate) async fn index() -> Html<String> {
    let html_content = include_str!("./index.html");

    Html(html_content.to_string())
}
