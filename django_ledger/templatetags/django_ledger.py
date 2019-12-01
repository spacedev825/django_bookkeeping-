from django import template

register = template.Library()


@register.inclusion_tag('django_ledger/tags/balance_sheet.html')
def balance_sheet(entity):
    bs_data = entity.balance_sheet()

    assets = [acc for acc in bs_data if acc['role_bs'] == 'assets']
    liabilities = [acc for acc in bs_data if acc['role_bs'] == 'liabilities']

    equity = [acc for acc in bs_data if acc['role_bs'] == 'equity']
    capital = [acc for acc in equity if acc['role'] in ['cap', 'capj']]
    earnings = [acc for acc in equity if acc['role'] in ['ex', 'in']]

    total_assets = sum(
        [acc['balance'] for acc in assets if acc['balance_type'] == 'debit'] +
        [-acc['balance'] for acc in assets if acc['balance_type'] == 'credit'])
    total_liabilities = sum(
        [acc['balance'] for acc in liabilities if acc['balance_type'] == 'credit'] +
        [-acc['balance'] for acc in liabilities if acc['balance_type'] == 'debit'])
    total_capital = sum(
        [acc['balance'] for acc in capital if acc['balance_type'] == 'credit'] +
        [-acc['balance'] for acc in capital if acc['balance_type'] == 'debit'])
    retained_earnings = sum(
        [acc['balance'] for acc in earnings if acc['balance_type'] == 'credit'] +
        [-acc['balance'] for acc in earnings if acc['balance_type'] == 'debit'])
    total_equity = total_capital + retained_earnings - total_liabilities
    total_liabilities_equity = total_liabilities + total_equity
    return {
        'bs_data': bs_data,

        'assets': assets,
        'total_assets': total_assets,

        'liabilities': liabilities,
        'total_liabilities': total_liabilities,

        'equity': equity,
        'total_equity': total_equity,

        'capital': capital,
        'total_capital': total_capital,

        'earnings': earnings,
        'retained_earnings': retained_earnings,

        'total_liabilities_equity': total_liabilities_equity
    }
