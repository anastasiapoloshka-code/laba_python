from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, selectinload
from database import engine
from laba_python.app.models import Base, User, Address, Product, Order

# Создаём таблицы если их нет
print("Создаём таблицы...")
Base.metadata.create_all(engine)
print("Таблицы созданы")

Session = sessionmaker(bind=engine)

print("Заполняем данными...")

# 1. ПОЛЬЗОВАТЕЛИ
print("Добавляем пользователей...")
with Session() as session:
    users = session.execute(select(User)).scalars().all()
    if not users:
        users_data = [
            {"username": "john_doe", "email": "john@example.com"},
            {"username": "jane_smith", "email": "jane@example.com"},
            {"username": "alice", "email": "alice@example.com"},
            {"username": "bob", "email": "bob@example.com"},
            {"username": "carol", "email": "carol@example.com"},
        ]
        for data in users_data:
            session.add(User(**data))
        session.commit()
        print("  5 пользователей добавлено")
    else:
        print(f"  Уже есть {len(users)} пользователей")

# 2. DESCRIPTION
print("Обновляем description...")
with Session() as session:
    users = session.execute(select(User)).scalars().all()
    descriptions = [
        "Любит путешествовать и фотографировать",
        "Программист и любитель кофе",
        "Книголюб и коллекционер винилов",
        "Спортсмен и вегетарианец",
        "Художник и музыкант"
    ]
    for i, user in enumerate(users):
        user.description = descriptions[i]
    session.commit()
    print("  Description обновлено")

# 3. ПРОДУКТЫ
print("Добавляем продукты...")
with Session() as session:
    products = session.execute(select(Product)).scalars().all()
    if not products:
        products_data = [
            {"name": "iPhone 15 Pro", "price": 999.99, "description": "Последняя модель Apple"},
            {"name": "MacBook Air M3", "price": 1299.99, "description": "Легкий и мощный ноутбук"},
            {"name": "AirPods Pro 2", "price": 249.99, "description": "Шумоподавление"},
            {"name": "Apple Watch Ultra", "price": 799.99, "description": "Для спорта"},
            {"name": "iPad Pro M4", "price": 1099.99, "description": "Мощный планшет"},
        ]
        for data in products_data:
            session.add(Product(**data))
        session.commit()
        print("  5 продуктов добавлено")
    else:
        print(f"  Уже есть {len(products)} продуктов")

# 4. АДРЕСА
print("Добавляем адреса...")
with Session() as session:
    addresses = session.execute(select(Address)).scalars().all()
    if not addresses:
        users = session.execute(select(User)).scalars().all()
        addresses_data = [
            {"user_id": users[0].id, "street": "Main St 1", "city": "New York", "country": "USA", "is_primary": True},
            {"user_id": users[1].id, "street": "Second Ave 5", "city": "Boston", "country": "USA", "is_primary": True},
            {"user_id": users[2].id, "street": "Baker St 221B", "city": "London", "country": "UK", "is_primary": True},
            {"user_id": users[3].id, "street": "Market Str 10", "city": "Berlin", "country": "Germany",
             "is_primary": True},
            {"user_id": users[4].id, "street": "Sunset Blvd 42", "city": "Los Angeles", "country": "USA",
             "is_primary": True},
        ]
        for data in addresses_data:
            session.add(Address(**data))
        session.commit()
        print("  5 адресов добавлено")
    else:
        print(f"  Уже есть {len(addresses)} адресов")

# 5. ЗАКАЗЫ
print("Создаём заказы...")
with Session() as session:
    orders = session.execute(select(Order)).scalars().all()
    if not orders:
        users = session.execute(select(User).options(selectinload(User.addresses))).scalars().all()
        products = session.execute(select(Product)).scalars().all()

        for i, user in enumerate(users[:5]):
            if i < len(products) and user.addresses:
                order = Order(
                    user_id=user.id,
                    address_id=user.addresses[0].id,
                    product_id=products[i].id,
                    quantity=1,
                    total_price=float(products[i].price)
                )
                session.add(order)
        session.commit()
        print("  5 заказов создано")
    else:
        print(f"  Уже есть {len(orders)} заказов")

print("\nВсе данные готовы")

# ВЫВОД РЕЗУЛЬТАТА (ИСПРАВЛЕННЫЙ БЛОК)
print("\n" + "=" * 70)
print("ЗАКАЗЫ С ПОЛНЫМИ ДАННЫМИ (selectinload)")
print("=" * 70)

with Session() as session:
    stmt = select(Order).options(
        selectinload(Order.user),
        selectinload(Order.address),
        selectinload(Order.product)
    )
    orders = session.execute(stmt).scalars().all()

    for order in orders:
        print(f"Заказ #{str(order.id)[:8]}")
        print(f"  Пользователь: {order.user.username}: {order.user.description[:30]}...")
        print(f"  Продукт: {order.product.name} x{order.quantity} = ${order.total_price}")
        print(f"  Адрес: {order.address.street}, {order.address.city}")
        print("-" * 70)
