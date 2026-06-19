import json, base64, os

img_dir = 'images/'
with open(img_dir + 'product_images.json') as f:
    img_map = json.load(f)

unique_imgs = set(img_map.values())
print(f'Converting {len(unique_imgs)} unique images to base64...')

b64_map = {}
for img_name in sorted(unique_imgs):
    path = img_dir + img_name
    if not os.path.exists(path):
        base = img_name.rsplit('.', 1)[0]
        for ext in ['.jpg', '.jpeg', '.png']:
            alt_path = img_dir + base + ext
            if os.path.exists(alt_path):
                path = alt_path
                break
    
    with open(path, 'rb') as f:
        data = f.read()
    
    ext = path.rsplit('.', 1)[1].lower()
    mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else 'image/png'
    b64 = base64.b64encode(data).decode('ascii')
    b64_map[img_name] = f'data:{mime};base64,{b64}'
    print(f'  {img_name}: {len(data)} bytes')

with open('img_base64.json', 'w') as f:
    json.dump(b64_map, f)

total = sum(len(v) for v in b64_map.values())
print(f'\nTotal base64 data: {total/1024:.0f}KB')
print('Saved to img_base64.json')
