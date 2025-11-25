import pandas as pd
import re

class FinancialChatbot:
    """
    AI-powered financial chatbot that answers predefined questions
    using financial data from Microsoft, Tesla, and Apple.
    """

    def __init__(self, file_path: str):
        self.data = pd.read_csv(file_path)
        self.prepare_data()

    def prepare_data(self):
        self.data['Fiscal Year'] = pd.to_numeric(self.data['Fiscal Year'], errors='coerce')
        self.data.dropna(inplace=True)

    def extract_company(self, user_input: str):
        companies = ['microsoft', 'apple', 'tesla']
        for company in companies:
            if company in user_input.lower():
                return company.capitalize()
        return None

    def extract_year(self, user_input: str):
        match = re.search(r'(20[0-9]{2})', user_input)
        return int(match.group(1)) if match else None

    def get_latest_year(self, company: str):
        return self.data[self.data['Company'] == company]['Fiscal Year'].max()

    def answer_query(self, user_input: str):
        company = self.extract_company(user_input)
        year = self.extract_year(user_input)

        if not company:
            return "Please specify a company: Microsoft, Apple, or Tesla."

        if not year:
            year = self.get_latest_year(company)

        row = self.data[
            (self.data['Company'] == company) &
            (self.data['Fiscal Year'] == year)
        ]

        if row.empty:
            return f"No data available for {company} in {year}."

        row = row.iloc[0]

        if "revenue" in user_input.lower():
            return f"{company} Revenue in {year}: ${row['Total Revenue']:,}"

        elif "net income" in user_input.lower() or "profit" in user_input.lower():
            return f"{company} Net Income in {year}: ${row['Net Income']:,}"

        elif "cash flow" in user_input.lower():
            return f"{company} Operating Cash Flow in {year}: ${row['Cash Flow from Operating Activities']:,}"

        elif "debt" in user_input.lower():
            ratio = (row['Total Liabilities'] / row['Total Assets']) * 100
            return f"{company} Debt Ratio in {year}: {ratio:.2f}%"

        elif "growth" in user_input.lower():
            return "Growth metrics are available in the financial analysis script."

        return "Sorry, I can answer questions about revenue, net income, cash flow, and debt ratio."


def main():
    chatbot = FinancialChatbot("data/MSFT_TSLA_AAPL.csv")

    print("\n AI Financial Chatbot\nType 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        response = chatbot.answer_query(user_input)
        print(f"Chatbot: {response}")


if __name__ == "__main__":
    main()
