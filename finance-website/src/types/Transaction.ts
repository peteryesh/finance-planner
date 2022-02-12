export interface Transaction {
    transaction_id: string;
    name: string;
    date: string; // YYYY-MM-DD
    amount: number;
    category: number;
    notes: string;
    account_id: string;
    username: string;
}