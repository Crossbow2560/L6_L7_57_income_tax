import pytest
from income_tax import taxable_income, tax_due, refund_status


# ---- taxable_income ----
def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_negative_gross():
    with pytest.raises(ValueError):
        taxable_income(-1, "new", 0)


def test_old_regime_investments_capped():
    # investments above 1.5L are capped: deduction = 50000 + 150000
    assert taxable_income(1000000, "old", 400000) == 800000


def test_unknown_regime():
    with pytest.raises(ValueError):
        taxable_income(500000, "foo", 0)


def test_deduction_exceeds_income():
    assert taxable_income(50000, "new", 0) == 0


# ---- tax_due ----
def test_below_exemption():
    assert tax_due(200000, 30) == 0


def test_negative_taxable():
    with pytest.raises(ValueError):
        tax_due(-1, 30)


def test_super_senior():
    assert tax_due(600000, 85) == 5000


def test_senior():
    assert tax_due(400000, 65) == 5000


def test_first_slab():
    assert tax_due(400000, 30) == 7500


def test_second_slab():
    assert tax_due(800000, 30) == 12500 + 300000 * 20 // 100


# ---- refund_status ----
def test_refund():
    assert refund_status(10000, 5000, True) == "refund"


def test_refund_delayed():
    assert refund_status(10000, 5000, False) == "refund delayed"


def test_pay_balance():
    assert refund_status(5000, 10000, True) == "pay balance"


def test_pay_balance_with_penalty():
    assert refund_status(5000, 10000, False) == "pay balance with penalty"


def test_settled():
    assert refund_status(5000, 5000, True) == "settled"
