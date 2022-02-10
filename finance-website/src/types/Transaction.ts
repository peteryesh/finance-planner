export interface Transaction {
    transaction_id: String;
    date: String; // YYYY-MM-DD
    amount: number;
    category: number;
    notes: String;
    account_id: String;
    username: String;
}