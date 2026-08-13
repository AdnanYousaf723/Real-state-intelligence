import pandas as pd
from pandera.errors import SchemaErrors
from typing import Tuple, Dict

from .schemas import raw_property_schema

class DataValidator:
    """Validates raw dataframes using Pandera schemas and generates quality reports."""
    
    def validate_properties(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
        """
        Validates raw property dataframe.
        Returns a tuple of: (valid_df, rejected_df, report_metrics)
        """
        try:
            # lazy=True ensures we collect all errors rather than failing on the first one
            valid_df = raw_property_schema.validate(df, lazy=True)
            rejected_df = pd.DataFrame(columns=df.columns)
            
            report = {
                "total": len(df),
                "valid": len(df),
                "rejected": 0,
                "errors": {}
            }
            return valid_df, rejected_df, report
            
        except SchemaErrors as err:
            failure_cases = err.failure_cases
            invalid_indices = failure_cases['index'].unique()
            
            # Split the dataframe into valid and rejected records
            valid_df = df.drop(index=invalid_indices)
            rejected_df = df.loc[invalid_indices]
            
            # Tabulate specific errors by column for the report
            errors_summary = failure_cases['column'].value_counts().to_dict()
            
            report = {
                "total": len(df),
                "valid": len(valid_df),
                "rejected": len(rejected_df),
                "errors": errors_summary
            }
            
            return valid_df, rejected_df, report

    @staticmethod
    def format_report(report: Dict) -> str:
        """Formats the validation report into a readable string summary."""
        lines = [
            "Validation Report",
            "────────────────────────────",
            f"Rows received:       {report['total']:>6}",
            f"Valid:               {report['valid']:>6}",
            f"Rejected:            {report['rejected']:>6}",
            ""
        ]
        
        if report['errors']:
            lines.append("Issues found by column:")
            for col, count in report['errors'].items():
                lines.append(f"{col:<20} {count:>6}")
                
        return "\n".join(lines)
