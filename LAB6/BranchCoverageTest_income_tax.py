import pytest
from income_tax import taxable_income, tax_due, refund_status


# ---- taxable_income ----
def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_negative_gross():
    with pytest.raises(ValueError):
        taxable_income(-1, "new", 0)


def test_zero_gross_not_invalid():
    # gross < 0 False branch at the boundary
    assert taxable_income(0, "new", 0) == 0


def test_old_regime_investments_capped():
    assert taxable_income(1000000, "old", 400000) == 800000


def test_old_regime_investments_at_cap():
    # investments == 150000: "> 150000" False branch, boundary
    assert taxable_income(1000000, "old", 150000) == 800000


def test_old_regime_investments_below_cap():
    assert taxable_income(1000000, "old", 50000) == 900000


def test_unknown_regime():
    with pytest.raises(ValueError):
        taxable_income(500000, "foo", 0)


def test_deduction_exceeds_income():
    assert taxable_income(50000, "new", 0) == 0


def test_deduction_equals_income():
    # taxable == 0: "taxable < 0" False branch, boundary
    assert taxable_income(75000, "new", 0) == 0


# ---- tax_due ----
def test_below_exemption():
    assert tax_due(200000, 30) == 0


def test_negative_taxable():
    with pytest.raises(ValueError):
        tax_due(-1, 30)


def test_zero_taxable():
    assert tax_due(0, 30) == 0


def test_age_80_boundary():
    assert tax_due(600000, 80) == 5000


def test_age_79_is_senior_not_super_senior():
    assert tax_due(600000, 79) == 22500


def test_age_60_boundary():
    assert tax_due(400000, 60) == 5000


def test_age_59_is_regular():
    assert tax_due(400000, 59) == 7500


def test_equal_to_exemption():
    # taxable == exempt: "<=" True branch at boundary
    assert tax_due(250000, 30) == 0
    assert tax_due(300000, 60) == 0
    assert tax_due(500000, 80) == 0


def test_first_slab():
    assert tax_due(400000, 30) == 7500


def test_slab_upper_boundary():
    # slab == 250000 exactly: still 5% slab
    assert tax_due(500000, 30) == 12500


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
    assert refund_status(5000, 5000, False) == "settled"
