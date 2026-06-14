export enum BudgetStatus {
  Draft = 'Draft',
  Active = 'Active',
  Locked = 'Locked',
  Archived = 'Archived',
}

export enum ExpenseStatus {
  Draft = 'Draft',
  Submitted = 'Submitted',
  Approved = 'Approved',
  Rejected = 'Rejected',
  Paid = 'Paid',
}

export enum PaymentMethod {
  Cash = 'Cash',
  BankTransfer = 'BankTransfer',
  Credit = 'Credit',
  Company = 'Company',
}

export enum SupplierStatus {
  Active = 'Active',
  Suspended = 'Suspended',
  Blacklisted = 'Blacklisted',
}

export enum BudgetCategory {
  Design = 'Design',
  Material = 'Material',
  Labor = 'Labor',
  Furniture = 'Furniture',
  Appliance = 'Appliance',
  Contingency = 'Contingency',
  Other = 'Other',
}
