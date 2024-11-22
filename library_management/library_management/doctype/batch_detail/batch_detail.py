# Copyright (c) 2024, Oduol Peris and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
import requests

class BatchDetail(Document):
    pass

@frappe.whitelist()
def fetch_and_create_batch_details():
    """
    Fetch batch details from an API and save them into the Batch Detail Doctype.
    """
    # API endpoint URL
    url = "http://65.21.156.159/api/accounting/batchdetails/2"

    # Initialize lists to track inserted and skipped batch IDs
    inserted_ids = []
    skipped_ids = []

    try:
        # Fetch data from the API
        response = requests.get(url)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Iterate through each batch in the response data
        for batch in data:
            # Check if the batch already exists
            if not frappe.db.exists("Batch Detail", {"batch_id": batch["id"]}):
                # Create a new Batch Detail document
                batch_doc = frappe.get_doc({
                    "doctype": "Batch Detail",
                    "batch_id": batch["id"],
                    "master_id": batch["master_id"],
                    "item": batch["Item"],
                    "weight": batch["Weight"],
                    "user": batch["user"],
                    "time": batch["time"],
                    "collections": batch["Collections"],
                })

                # Save the document in the database
                batch_doc.insert()
                inserted_ids.append(batch["id"])  # Add to inserted list
            else:
                skipped_ids.append(batch["id"])  # Add to skipped list

        # Commit the transaction to the database
        frappe.db.commit()

        # Log success
        frappe.logger().info(f"Batch details successfully fetched. Inserted: {inserted_ids}, Skipped: {skipped_ids}")
        return {"status": "success", "inserted_batches": inserted_ids, "skipped_batches": skipped_ids}

    except requests.exceptions.RequestException as e:
        frappe.logger().error(f"API request error: {e}")
        return {"status": "error", "message": f"API request failed: {e}"}
    except Exception as e:
        frappe.logger().error(f"Processing error: {e}")
        return {"status": "error", "message": f"Internal error occurred: {e}"}
