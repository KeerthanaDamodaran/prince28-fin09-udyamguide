import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from udyamguide.config import get_settings


async def main():
    engine = create_async_engine(get_settings().database_url)

    async with engine.connect() as conn:
        print("\n===== DOCUMENT PARSING SUMMARY =====")

        result = await conn.execute(
            text("""
            SELECT
                title,
                doc_type,
                metadata->>'parser' AS parser,
                metadata->>'pages' AS pages,
                metadata->>'tables' AS tables
            FROM documents
            WHERE doc_type <> 'record'
            ORDER BY id DESC
            LIMIT 20
        """)
        )

        for row in result:
            print(dict(row._mapping))

        print("\n===== EXTRACTED PAGE CONTENT =====")

        result = await conn.execute(
            text("""
            SELECT
                d.title,
                p.page_no,
                p.headings,
                LEFT(p.text, 600) AS start_of_page
            FROM pages p
            JOIN documents d ON d.id = p.document_id
            ORDER BY p.id DESC
            LIMIT 5
        """)
        )

        for row in result:
            print("\n------------------------------")
            print("Document:", row.title)
            print("Page:", row.page_no)
            print("Headings:", row.headings)
            print("Extracted text:", row.start_of_page)

    await engine.dispose()


asyncio.run(main())
