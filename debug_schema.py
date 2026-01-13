try:
    print("Importing product_schema...")
    from app.schemas.product_schema import ProductType
    print("Imported ProductType")
    
    print("Importing cart_schema...")
    from app.schemas.cart_schema import CartItem
    print("Imported CartItem")
    
    print("Success")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
