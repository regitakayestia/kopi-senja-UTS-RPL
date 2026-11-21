import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); 
    for name,w,h in [("03a-usecase",1240,1000),("03c-activity",850,990)]:
        pg=b.new_page(viewport={"width":w,"height":h},device_scale_factor=2)
        pg.goto(f"file:///home/claude/kopi-senja/docs/diagrams/{name}.svg"); pg.screenshot(path=f"/home/claude/kopi-senja/docs/diagrams/{name}.png")
    b.close()
