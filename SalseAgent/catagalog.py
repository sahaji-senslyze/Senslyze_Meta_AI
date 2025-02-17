# let's set up a dummy product catalog:
sample_product_catalog = """
Sleep Haven product 1: Luxury Cloud-Comfort Memory Foam Mattress
Experience the epitome of opulence with our Luxury Cloud-Comfort Memory Foam Mattress. Designed with an innovative, temperature-sensitive memory foam layer, this mattress embraces your body shape, offering personalized support and unparalleled comfort. The mattress is completed with a high-density foam base that ensures longevity, maintaining its form and resilience for years. With the incorporation of cooling gel-infused particles, it regulates your body temperature throughout the night, providing a perfect cool slumbering environment. The breathable, hypoallergenic cover, exquisitely embroidered with silver threads, not only adds a touch of elegance to your bedroom but also keeps allergens at bay. For a restful night and a refreshed morning, invest in the Luxury Cloud-Comfort Memory Foam Mattress.
Price: $999
Sizes available for this product: Twin, Queen, King

Sleep Haven product 2: Classic Harmony Spring Mattress
A perfect blend of traditional craftsmanship and modern comfort, the Classic Harmony Spring Mattress is designed to give you restful, uninterrupted sleep. It features a robust inner spring construction, complemented by layers of plush padding that offers the perfect balance of support and comfort. The quilted top layer is soft to the touch, adding an extra level of luxury to your sleeping experience. Reinforced edges prevent sagging, ensuring durability and a consistent sleeping surface, while the natural cotton cover wicks away moisture, keeping you dry and comfortable throughout the night. The Classic Harmony Spring Mattress is a timeless choice for those who appreciate the perfect fusion of support and plush comfort.
Price: $1,299
Sizes available for this product: Queen, King

Sleep Haven product 3: EcoGreen Hybrid Latex Mattress
The EcoGreen Hybrid Latex Mattress is a testament to sustainable luxury. Made from 100% natural latex harvested from eco-friendly plantations, this mattress offers a responsive, bouncy feel combined with the benefits of pressure relief. It is layered over a core of individually pocketed coils, ensuring minimal motion transfer, perfect for those sharing their bed. The mattress is wrapped in a certified organic cotton cover, offering a soft, breathable surface that enhances your comfort. Furthermore, the natural antimicrobial and hypoallergenic properties of latex make this mattress a great choice for allergy sufferers. Embrace a green lifestyle without compromising on comfort with the EcoGreen Hybrid Latex Mattress.
Price: $1,599
Sizes available for this product: Twin, Full

Sleep Haven product 4: Plush Serenity Bamboo Mattress
The Plush Serenity Bamboo Mattress takes the concept of sleep to new heights of comfort and environmental responsibility. The mattress features a layer of plush, adaptive foam that molds to your body's unique shape, providing tailored support for each sleeper. Underneath, a base of high-resilience support foam adds longevity and prevents sagging. The crowning glory of this mattress is its bamboo-infused top layer - this sustainable material is not only gentle on the planet, but also creates a remarkably soft, cool sleeping surface. Bamboo's natural breathability and moisture-wicking properties make it excellent for temperature regulation, helping to keep you cool and dry all night long. Encased in a silky, removable bamboo cover that's easy to clean and maintain, the Plush Serenity Bamboo Mattress offers a luxurious and eco-friendly sleeping experience.
Price: $2,599
Sizes available for this product: King

Sleep Haven product 5: UltraPlush Euro-Top Mattress
Indulge in cloud-like comfort with the UltraPlush Euro-Top Mattress. This premium mattress is topped with a thick layer of cushiony foam, designed to cradle your body and relieve pressure points. Beneath the plush surface lies a core of individually wrapped coils that deliver precise support, adjusting to your body's needs as you sleep. The Euro-Top design ensures a smooth, even surface from edge to edge, so you can enjoy the same level of comfort across the entire mattress. With its hypoallergenic pillow-top cover and moisture-wicking fibers, the UltraPlush Euro-Top Mattress promises a dry, cool, and restful night’s sleep.
Price: $1,899
Sizes available for this product: Full, Queen, King

Sleep Haven product 6: Firm Support Orthopedic Mattress
Ideal for those who need extra back support, the Firm Support Orthopedic Mattress provides exceptional firmness without sacrificing comfort. Its high-density foam construction delivers targeted support for your spine, ensuring proper alignment and reducing discomfort. The mattress also features an anti-sag reinforced edge design, preventing roll-offs and ensuring durability for years to come. Its breathable cover, made from bamboo-charcoal fibers, naturally wicks away moisture and prevents odors, creating a clean and healthy sleep environment. For those seeking a therapeutic sleep experience, the Firm Support Orthopedic Mattress is the perfect solution.
Price: $1,499
Sizes available for this product: Twin, Queen, King

Sleep Haven product 7: CoolRest Gel-Infused Mattress
Sleep cool and comfortably with the CoolRest Gel-Infused Mattress. Designed with layers of gel memory foam, this mattress adapts to your body’s contours while keeping heat at bay. The gel-infused top layer disperses heat, ensuring you remain cool throughout the night. Underneath, a high-density foam base offers stability and support, making this mattress ideal for all types of sleepers. The quilted, moisture-wicking cover is removable and washable, making it easy to maintain. Whether you're a hot sleeper or just looking for a refreshing sleep experience, the CoolRest Gel-Infused Mattress is your best bet.
Price: $1,099
Sizes available for this product: Twin, Queen, King

Sleep Haven product 8: SnugNest Crib Mattress
For your little one, Sleep Haven introduces the SnugNest Crib Mattress, designed with safety and comfort in mind. This mattress features dual-sided firmness: one firm side for newborns and one softer side for toddlers. The breathable foam core provides consistent support, while the waterproof cover protects against spills and accidents. Made from hypoallergenic materials, it helps prevent allergens and dust mites, ensuring your baby sleeps in a healthy environment. The SnugNest Crib Mattress is lightweight and easy to clean, making it a parent’s favorite.
Price: $299
Sizes available for this product: Crib

Sleep Haven product 9: Therapeutic Lavender-Infused Memory Foam Mattress
Soothe your senses as you sleep with the Therapeutic Lavender-Infused Memory Foam Mattress. This innovative mattress is infused with natural lavender oils, known for their calming and stress-relieving properties. The contouring memory foam layers offer plush support while evenly distributing body weight, reducing pressure points. Its lavender-infused cover emits a subtle, soothing aroma, creating a tranquil sleep environment. Ideal for those who struggle with stress or insomnia, the Therapeutic Lavender-Infused Memory Foam Mattress offers a perfect combination of relaxation and support.
Price: $1,699
Sizes available for this product: Queen, King

Sleep Haven product 10: Adjustable Comfort Sleep System
Take control of your sleep experience with the Adjustable Comfort Sleep System. This fully adjustable mattress features a split design, allowing each side to be customized to individual preferences. Whether you prefer a soft or firm surface, the adjustable air chambers within the mattress allow for personalized comfort. The bed can also be elevated at both the head and foot, providing relief from snoring, acid reflux, and joint pain. The mattress is topped with a layer of cooling gel memory foam for additional comfort, ensuring you stay cool even when elevated. With a wireless remote and a smart app, the Adjustable Comfort Sleep System gives you full control of your sleep experience.
Price: $3,299
Sizes available for this product: Queen, King

"""
with open("sample_product_catalog.txt", "w") as f:
    f.write(sample_product_catalog)

product_catalog = "sample_product_catalog.txt"