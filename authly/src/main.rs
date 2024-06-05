use tracing_subscriber::{EnvFilter, fmt};
use tracing_subscriber::layer::SubscriberExt;
use tracing_subscriber::util::SubscriberInitExt;

mod log;
mod routes;


struct AppState {
    
}


#[tokio::main]
async fn main()-> Result<(), Box<dyn std::error::Error>> {
    init_tracing();

    println!("Hello, world!");
    let port = "8000";

    let origins = [
        "http://192.168.178.58".parse().unwrap(),
    ];

    let listener = tokio::net::TcpListener::bind(format!("0.0.0.0:{}", &port))
        .await
        .unwrap();


    tracing::info!("Server Running on: {}", port);

    axum::serve(listener, routes::configure_routes(origins))
        .await
        .expect("Failed to run Axum server");

    Ok(())
}


//noinspection GrazieInspection
#[inline(always)]
fn init_tracing() {
    // human_panic::setup_panic!(
    //     human_panic::Metadata::new(env!("CARGO_PKG_NAME"), env!("CARGO_PKG_VERSION"))
    //         .authors("Arteii <ben.arteii@proton.me>")
    //         .homepage("https://github.com/Arteiii/authly")
    //         .support("- Open a support request at https://github.com/Arteiii/authly/issues/new")
    // );
    tracing_subscriber::registry()
        .with(fmt::layer())
        .with(EnvFilter::from_default_env())
        .init();
}
