use std::process::Command;
use std::io::{self, Write};
use clap::Parser;
use reqwest::Client;
use serde_json::json;
use futures_util::StreamExt;
use anyhow::Result;
use dirs;

#[derive(Parser)]
struct Args {
    /// Include system logs
    #[arg(long)]
    logs: bool,

    /// Include shell history
    #[arg(long)]
    history: bool,

    /// Include man page of the given command
    #[arg(long)]
    man: Option<String>,

    /// Choose Ollama model
    #[arg(long, default_value = "tinyllama")]
    model: String,
}

#[tokio::main]
async fn main() -> Result<()> {
    let args = Args::parse();

    let mut context = String::new();

    if args.logs {
        let logs = std::fs::read_to_string("/var/log/syslog").unwrap_or_else(|_| "Could not read system logs.".into());
        context.push_str(&format!("\nLogs:\n{}", logs));
    }

    if args.history {
        if let Some(home) = dirs::home_dir() {
            let history = std::fs::read_to_string(home.join(".bash_history")).unwrap_or_else(|_| "Could not read bash history.".into());
            context.push_str(&format!("\nHistory:\n{}", history));
        }
    }

    if let Some(man_cmd) = &args.man {
        let output = Command::new("man")
        .arg(man_cmd)
        .output()
        .unwrap_or_else(|_| panic!("Failed to run man {}", man_cmd));
        let man_page = String::from_utf8_lossy(&output.stdout);
        context.push_str(&format!("\nMan Page for {}:\n{}", man_cmd, man_page));
    }

    // Get user input
    print!("Enter your question or extra info:\n> ");
    io::stdout().flush()?;

    let mut input = String::new();
    io::stdin().read_line(&mut input)?;

    let prompt = format!(
        "You are a friendly Linux assistant. Be concise, clear, step-by-step.\n\nContext:{}\n\nInput:\n{}",
        context,
        input.trim()
    );

    let client = Client::new();

    let body = json!({
        "model": args.model,
        "stream": true,
        "messages": [
            {"role": "system", "content": "You help troubleshoot Linux commands."},
            {"role": "user", "content": prompt}
        ]
    });

    let response = client
    .post("http://localhost:11434/api/chat")
    .json(&body)
    .send()
    .await?;

    let mut stream = response.bytes_stream();

    println!("\nAnswer:\n");

    while let Some(chunk) = stream.next().await {
        let chunk = chunk?;
        let chunk_str = String::from_utf8_lossy(&chunk);
        for line in chunk_str.lines() {
            if let Ok(json_line) = serde_json::from_str::<serde_json::Value>(line) {
                if let Some(content) = json_line["message"]["content"].as_str() {
                    print!("{}", content);
                    io::stdout().flush()?;
                }
            }
        }
    }

    Ok(())
}
