import sys
import time
from rich.console import Console
from pynput import keyboard

from data_fetcher import get_stock_data
from k_chart import KChart

class AppState:
    """Manages the application's state."""
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.timeframes = ["1d", "1wk", "1mo"]
        self.timeframe_names = {"1d": "Daily", "1wk": "Weekly", "1mo": "Monthly"}
        self.timeframe_idx = 0
        self.data = {}
        self.should_exit = False
        self.console = Console()
        self._load_data()

    def _load_data(self):
        """Loads data for all timeframes."""
        with self.console.status(f"[bold green]Fetching data for {self.ticker.upper()}...") as status:
            # Daily data for 2 years
            daily_data = get_stock_data(self.ticker, period="2y", interval="1d")
            if daily_data.empty:
                raise ValueError(f"Could not fetch daily data for {self.ticker}.")
            self.data["1d"] = daily_data

            # Resample daily data for weekly and monthly views
            self.data["1wk"] = self._resample_data(daily_data, "W")
            self.data["1mo"] = self._resample_data(daily_data, "M")
            
            self.console.print(f"[green]✓[/green] Data loaded for {self.ticker.upper()}.")

    def _resample_data(self, df, rule):
        """Resamples OHLC data to a different timeframe."""
        ohlc_dict = {
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }
        resampled_df = df.resample(rule).apply(ohlc_dict).dropna()
        return resampled_df

    def next_timeframe(self):
        self.timeframe_idx = (self.timeframe_idx + 1) % len(self.timeframes)

    def prev_timeframe(self):
        self.timeframe_idx = (self.timeframe_idx - 1 + len(self.timeframes)) % len(self.timeframes)

    def get_current_data(self):
        tf = self.timeframes[self.timeframe_idx]
        return self.data.get(tf)

    def get_current_title(self):
        tf = self.timeframes[self.timeframe_idx]
        name = self.timeframe_names[tf]
        return f"{self.ticker.upper()} - {name} Chart"

def on_press(key, state: AppState):
    """Keyboard press event handler."""
    if key == keyboard.Key.left:
        state.prev_timeframe()
    elif key == keyboard.Key.right:
        state.next_timeframe()

def on_release(key, state: AppState):
    """Keyboard release event handler."""
    if key == keyboard.Key.esc:
        state.should_exit = True
        return False  # Stop listener

def main():
    """Main application entry point."""
    console = Console()
    
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    else:
        ticker = console.input("[bold]Enter a stock ticker (e.g., AAPL): [/bold]")

    if not ticker:
        console.print("[bold red]Error: Ticker symbol cannot be empty.[/bold red]")
        sys.exit(1)

    try:
        app_state = AppState(ticker)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)

    # Start keyboard listener
    listener = keyboard.Listener(
        on_press=lambda key: on_press(key, app_state),
        on_release=lambda key: on_release(key, app_state)
    )
    listener.start()

    console.print("Controls: ← → to change timeframe | Esc to exit.")
    time.sleep(2) # Show controls message

    try:
        while not app_state.should_exit:
            data = app_state.get_current_data()
            if data is not None and not data.empty:
                chart = KChart(data)
                title = app_state.get_current_title()
                chart.render(title)
            else:
                console.clear()
                console.print(f"No data for timeframe {app_state.timeframes[app_state.timeframe_idx]}", justify="center")
            
            # Redraw every second to handle terminal resize
            time.sleep(1) 
    except KeyboardInterrupt:
        app_state.should_exit = True
    finally:
        listener.stop()
        listener.join()
        console.clear()
        console.print("[bold cyan]Goodbye![/bold cyan]")

if __name__ == "__main__":
    main() 