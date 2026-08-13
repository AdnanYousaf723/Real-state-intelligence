import os
import requests
import pandas as pd
from typing import Optional
from reli.ingestion.base import DataSource
import logging

logger = logging.getLogger(__name__)

class ATTOMDataSource(DataSource):
    """
    Adapter for the ATTOM Developer API.
    Provides real property data via REST endpoints.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.gateway.attomdata.com/propertyapi/v1.0.0"):
        # Use provided key or fallback to environment variable
        self.api_key = api_key or os.getenv("ATTOM_API_KEY")
        self.base_url = base_url
        self.headers = {
            "apikey": self.api_key,
            "Accept": "application/json"
        }

    def fetch(self, address: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Fetches property data from ATTOM.
        For MVP, we support fetching by a single address or a predefined list if no params are given.
        """
        if not self.api_key:
            logger.warning("No ATTOM API key provided. Returning empty dataframe.")
            return pd.DataFrame()

        try:
            # If no specific address is provided, we fetch a few demo addresses to simulate a batch
            addresses_to_fetch = [address] if address else [
                "4529 Winona Court, Denver, CO",
                "123 Main St, Denver, CO"
            ]
            
            records = []
            for addr in addresses_to_fetch:
                url = f"{self.base_url}/property/detail?address={addr}"
                response = requests.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    data = response.json()
                    props = data.get("property", [])
                    for p in props:
                        # Flatten ATTOM's nested JSON into a flat dict compatible with our canonical mapper
                        address_info = p.get("address", {})
                        summary = p.get("summary", {})
                        building = p.get("building", {})
                        size = building.get("size", {})
                        rooms = building.get("rooms", {})
                        sale = p.get("sale", {})
                        
                        flat_record = {
                            "raw_address": address_info.get("oneLine"),
                            "city": address_info.get("locality"),
                            "state": address_info.get("countrySubd"),
                            "zip_code": address_info.get("postal1"),
                            "property_type": summary.get("propclass"),
                            "year_built": summary.get("yearbuilt"),
                            "last_sale_price": sale.get("saleSearchSetup", {}).get("saleTrans", {}).get("saleAmt"),
                            "last_sale_date": sale.get("saleSearchSetup", {}).get("saleTrans", {}).get("recordingDate"),
                            "absentee_owner": str(summary.get("absenteeInd", "")).lower() == "absentee",
                            "is_vacant": False # ATTOM doesn't guarantee a simple vacancy flag here without enriched endpoints
                        }
                        records.append(flat_record)
                else:
                    logger.error(f"ATTOM API error {response.status_code} for {addr}: {response.text}")
                    
            return pd.DataFrame(records)
            
        except Exception as e:
            logger.error(f"Failed to fetch data from ATTOM: {e}")
            return pd.DataFrame()
