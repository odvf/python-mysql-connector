#!/usr/bin/env python3

import argparse
import sys
import json
import csv
import io
from typing import Dict, List, Any, Optional
import mysql.connector
from mysql.connector import Error


class MySQLClient:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self) -> bool:
        """Establish connection to MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}", file=sys.stderr)
            return False

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute SQL query and return results in a structured format."""
        if not self.connection or not self.connection.is_connected():
            return {"error": "Not connected to database"}

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)

            # Handle different types of queries
            if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN')):
                results = cursor.fetchall()
                return {
                    "status": "success",
                    "query": query,
                    "rows_returned": len(results),
                    "data": results,
                    "columns": [desc[0] for desc in cursor.description] if cursor.description else []
                }
            else:
                # For INSERT, UPDATE, DELETE, etc.
                return {
                    "status": "success",
                    "query": query,
                    "rows_affected": cursor.rowcount,
                    "data": None,
                    "columns": []
                }

        except Error as e:
            return {
                "status": "error",
                "query": query,
                "error": str(e),
                "data": None,
                "columns": []
            }
        finally:
            if 'cursor' in locals():
                cursor.close()

    def close(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()


class OutputFormatter:
    @staticmethod
    def format_json(data: Dict[str, Any], pretty: bool = False) -> str:
        """Format output as JSON."""
        if pretty:
            return json.dumps(data, indent=2, default=str)
        return json.dumps(data, default=str)

    @staticmethod
    def format_csv(data: Dict[str, Any]) -> str:
        """Format output as CSV."""
        if data.get("status") != "success" or not data.get("data"):
            return OutputFormatter.format_json(data)

        output = io.StringIO()
        if data["data"]:
            writer = csv.DictWriter(output, fieldnames=data["columns"])
            writer.writeheader()
            writer.writerows(data["data"])

        return output.getvalue()

    @staticmethod
    def format_table(data: Dict[str, Any]) -> str:
        """Format output as a simple table."""
        if data.get("status") != "success" or not data.get("data"):
            return OutputFormatter.format_json(data, pretty=True)

        if not data["data"]:
            return "No data returned."

        columns = data["columns"]
        rows = data["data"]

        # Calculate column widths
        widths = {}
        for col in columns:
            widths[col] = len(str(col))

        for row in rows:
            for col in columns:
                widths[col] = max(widths[col], len(str(row.get(col, ""))))

        # Create table
        result = []

        # Header
        header = " | ".join(str(col).ljust(widths[col]) for col in columns)
        result.append(header)
        result.append("-" * len(header))

        # Rows
        for row in rows:
            row_str = " | ".join(str(row.get(col, "")).ljust(widths[col]) for col in columns)
            result.append(row_str)

        # Summary
        result.append("")
        result.append(f"Rows returned: {data['rows_returned']}")

        return "\n".join(result)


def read_from_stdin() -> Optional[str]:
    """Read query from stdin if available."""
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None


def main():

    parser = argparse.ArgumentParser(
        description="MySQL Command Line Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 connector.py -t localhost -u root -p password -d mydb -q "SELECT * FROM users"
  echo "SELECT COUNT(*) FROM products" | python3 connector.py -t 192.168.1.100 -u admin -p secret -d inventory
  python3 connector.py -t db.example.com -u user -p 'pass@123' -d app -r 3306 -q "SHOW TABLES" -f table
  cat query.sql | python3 connector.py -t db.server.com -u admin -p secret -d production
        """
    )

    # Database connection arguments
    parser.add_argument("-t", "--host", required=True, help="MySQL host")
    parser.add_argument("-u", "--user", required=True, help="MySQL username")
    parser.add_argument("-p", "--password", required=True, help="MySQL password")
    parser.add_argument("-d", "--database", required=True, help="MySQL database name")
    parser.add_argument("-r", "--port", type=int, default=3306, help="MySQL port (default: 3306)")

    # Query arguments
    parser.add_argument("-q", "--query", help="SQL query to execute")

    # Output format arguments
    parser.add_argument("-f", "--format", choices=["json", "csv", "table"], default="json",
                       help="Output format (default: json)")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON output")

    # Parse arguments
    args = parser.parse_args()

    print(args)

    # Get query from command line or stdin
    query = args.query
    if not query:
        query = read_from_stdin()

    if not query:
        print("Error: No query provided. Use -q option or pipe query through stdin.", file=sys.stderr)
        sys.exit(1)

    # Create MySQL client and connect
    client = MySQLClient(args.host, args.user, args.password, args.database, args.port)

    if not client.connect():
        sys.exit(1)

    try:
        # Execute query
        result = client.execute_query(query)

        # Format and output result
        formatter = OutputFormatter()

        if args.format == "json":
            output = formatter.format_json(result, args.pretty)
        elif args.format == "csv":
            output = formatter.format_csv(result)
        elif args.format == "table":
            output = formatter.format_table(result)

        print(output)

        # Exit with error code if query failed
        if result.get("status") == "error":
            sys.exit(1)

    finally:
        client.close()

if __name__ == "__main__":
    main()
