use axum::response::Redirect;

pub(crate) async fn wiki() -> Redirect {
    Redirect::permanent("https://github.com/Arteiii/Authly/wiki")
}

pub(crate) async fn github() -> Redirect {
    Redirect::permanent("https://github.com/Arteiii/Authly")
}
