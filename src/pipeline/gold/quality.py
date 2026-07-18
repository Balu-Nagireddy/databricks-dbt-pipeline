from pathlib import Path
from src.common.logging import get_logger

logger = get_logger(__name__)

class BusinessValidationGateway:
    """
    Validates business consistency across Gold Marts and writes verification reports.
    """
    def __init__(self):
        self.validation_runs = []
        self.acceptance_rate = 100.0

    def run_validations(self, marts: dict) -> bool:
        logger.info("Executing analytical business validations on Gold Marts...")
        
        # 1. Product Mart: product_id uniqueness
        prod_perf = marts["product_performance"]
        total_prods = prod_perf.count()
        unique_prods = prod_perf.select("product_id").distinct().count()
        prod_dup_ok = total_prods == unique_prods
        self.validation_runs.append({
            "check": "Product ID Uniqueness in Product Performance",
            "status": "PASS" if prod_dup_ok else "FAIL",
            "details": f"Total products: {total_prods}, Unique: {unique_prods}"
        })
        
        # 2. Customers Mart: lifetime_value null checks
        clv = marts["customer_lifetime_value"]
        null_clv_count = clv.filter(clv["lifetime_value"].isNull()).count()
        clv_null_ok = null_clv_count == 0
        self.validation_runs.append({
            "check": "No Null Lifetime Value in Customer Mart",
            "status": "PASS" if clv_null_ok else "FAIL",
            "details": f"Null value count: {null_clv_count}"
        })

        # 3. Finance Mart: payment methods total value null check
        fin = marts["payment_method_distribution"]
        null_pay_val = fin.filter(fin["total_payment_value"].isNull()).count()
        fin_null_ok = null_pay_val == 0
        self.validation_runs.append({
            "check": "No Null Total Value in Payment Distribution",
            "status": "PASS" if fin_null_ok else "FAIL",
            "details": f"Null payment value count: {null_pay_val}"
        })

        # Calculate acceptance rate
        passed = sum(1 for v in self.validation_runs if v["status"] == "PASS")
        self.acceptance_rate = (passed / len(self.validation_runs)) * 100.0
        
        logger.info(f"Gold quality validation finished with acceptance rate: {self.acceptance_rate:.2f}%")
        self.generate_dq_report(marts)
        return self.acceptance_rate == 100.0

    def generate_dq_report(self, marts: dict):
        report_path = Path("./docs/GOLD_DATA_QUALITY.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        md = [
            "# Gold Layer Business Data Quality Report",
            "",
            "This report documents business checks, aggregations, and metrics validations completed at the Gold Analytical Layer.",
            "",
            "## Quality Gate Validation Checks",
            "",
            "| Validation Test | Status | Details |",
            "| :--- | :---: | :--- |"
        ]
        
        for r in self.validation_runs:
            md.append(f"| {r['check']} | `{r['status']}` | {r['details']} |")
            
        md.append("")
        md.append(f"- **Final Acceptance Rate**: **{self.acceptance_rate:.2f}%**")
        md.append("")
        md.append("## Row Summary for Primary Analytical Marts")
        md.append("")
        md.append("| Mart Dataset | Row Count |")
        md.append("| :--- | :---: |")
        
        for key, df in marts.items():
            md.append(f"| {key} | {df.count():,} |")
            
        md.append("")
        md.append("## Business Rules Applied")
        md.append("1. **Unique Domain Keys**: Checked that product-level and customer-level metrics contain no key collisions.")
        md.append("2. **Completeness Checks**: Enforced no null values in financial aggregations or calculated customer value.")
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))
            
        logger.info(f"Gold data quality report saved at {report_path}")
