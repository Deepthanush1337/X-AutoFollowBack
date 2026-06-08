import main
import asyncio
if __name__ == "__main__":
    try:
        asyncio.run(main.main())
    except Exception as e:
        print(f"❌ Error: {e}")