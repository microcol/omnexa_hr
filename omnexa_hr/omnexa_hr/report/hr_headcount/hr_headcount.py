import frappe


def execute(filters=None):
	filters = frappe._dict(filters or {})

	columns = [
		{"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 180},
		{"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 150},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": "Headcount", "fieldname": "headcount", "fieldtype": "Int", "width": 120},
	]

	conditions = ["1=1"]
	params = {}

	if filters.get("company"):
		conditions.append("e.company = %(company)s")
		params["company"] = filters.company

	if filters.get("branch"):
		conditions.append("e.branch = %(branch)s")
		params["branch"] = filters.branch

	if filters.get("status"):
		conditions.append("e.status = %(status)s")
		params["status"] = filters.status

	data = frappe.db.sql(
		f"""
		SELECT
			e.company,
			e.branch,
			COALESCE(e.status, 'Unknown') AS status,
			COUNT(e.name) AS headcount
		FROM `tabEmployee` e
		WHERE {" AND ".join(conditions)}
		GROUP BY e.company, e.branch, e.status
		ORDER BY e.company, e.branch, e.status
		""",
		params,
		as_dict=True,
	)

	return columns, data

