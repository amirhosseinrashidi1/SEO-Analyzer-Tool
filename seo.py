import asyncio
import aiohttp
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from tkinter import ttk  # اضافه کردن این خط برای استفاده از Progressbar
from urllib.parse import urlparse
import time
import ssl
import json
import os
import threading

# متغیر سراسری برای ذخیره نتایج تحلیل
results = {}

# استفاده از کتابخانه asyncio و aiohttp برای درخواست‌های غیرهمزمان
async def fetch_website_data_async(url, session):
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()  # Check for HTTP errors
            return await response.text()
    except Exception as e:
        return f"Error fetching URL: {e}"

async def fetch_head_data_async(url, session):
    try:
        async with session.head(url, timeout=5) as response:
            response.raise_for_status()
            return response
    except Exception as e:
        return None

async def analyze_seo_async(url, html_content, session):
    soup = BeautifulSoup(html_content, 'html.parser')

    # بررسی زمان بارگذاری سایت
    start_time = time.time()
    response = await session.get(url, timeout=10)
    load_time = time.time() - start_time

    # بررسی عنوان‌ها و متا داده‌ها
    title = soup.title.string if soup.title else "No title found"
    meta_description = "No meta description found"
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_description = meta_tag["content"]

    # بررسی تگ‌های alt در تصاویر
    images = soup.find_all("img")
    images_without_alt = len([img for img in images if not img.get("alt")])

    # بررسی وضعیت HTTP Headers
    headers = {}
    try:
        async with session.head(url, timeout=5) as response:
            headers = response.headers
    except Exception:
        pass

    # بررسی لینک‌های شکسته
    broken_links = 0
    domain = urlparse(url).netloc
    for link in soup.find_all("a", href=True):
        href = link['href']
        if href.startswith("http"):
            try:
                link_response = await fetch_head_data_async(href, session)
                if link_response and link_response.status >= 400:
                    broken_links += 1
            except:
                broken_links += 1

    # بررسی تگ‌های Canonical
    canonical_url = "No canonical URL found"
    canonical_tag = soup.find("link", rel="canonical")
    if canonical_tag and canonical_tag.get("href"):
        canonical_url = canonical_tag["href"]

    # بررسی Sitemap و Robots.txt
    sitemap_status = "No sitemap.xml found"
    try:
        sitemap_response = await session.get(f"{url}/sitemap.xml", timeout=5)
        if sitemap_response.status == 200:
            sitemap_status = "sitemap.xml found"
    except:
        pass

    robots_status = "No robots.txt found"
    try:
        robots_response = await session.get(f"{url}/robots.txt", timeout=5)
        if robots_response.status == 200:
            robots_status = "robots.txt found"
    except:
        pass

    # بررسی SSL/TLS
    ssl_status = "No SSL/TLS"
    try:
        async with session.get(url, ssl=True, timeout=5) as response:
            ssl_status = "SSL/TLS is configured"
    except Exception:
        ssl_status = "SSL/TLS is not configured"

    return {
        "title": title,
        "meta_description": meta_description,
        "load_time": load_time,
        "images_without_alt": images_without_alt,
        "broken_links": broken_links,
        "canonical_url": canonical_url,
        "sitemap_status": sitemap_status,
        "robots_status": robots_status,
        "ssl_status": ssl_status,
        "headers": headers,
    }

async def analyze_url_async(url, progress_callback=None):
    global results
    async with aiohttp.ClientSession() as session:
        html_content = await fetch_website_data_async(url, session)
        if html_content.startswith("Error"):
            messagebox.showerror("Error", html_content)
            return

        results = await analyze_seo_async(url, html_content, session)

        if progress_callback:
            progress_callback(100)

        display_results(results)

def display_results(results):
    result_window = tk.Toplevel()
    result_window.title("SEO Analysis Results")

    result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=100, height=40)
    result_text.insert(tk.END, f"Title: {results['title']}\n")
    result_text.insert(tk.END, f"Meta Description: {results['meta_description']}\n")
    result_text.insert(tk.END, f"Load Time: {results['load_time']} seconds\n")
    result_text.insert(tk.END, f"Images without Alt: {results['images_without_alt']}\n")
    result_text.insert(tk.END, f"Broken Links: {results['broken_links']}\n")
    result_text.insert(tk.END, f"Canonical URL: {results['canonical_url']}\n")
    result_text.insert(tk.END, f"Sitemap Status: {results['sitemap_status']}\n")
    result_text.insert(tk.END, f"Robots.txt Status: {results['robots_status']}\n")
    result_text.insert(tk.END, f"SSL/TLS Status: {results['ssl_status']}\n")

    result_text.configure(state='disabled')
    result_text.pack(padx=10, pady=10)

def save_report(results):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(results, json_file, indent=4)
        messagebox.showinfo("Success", f"Report saved to {file_path}")

def analyze_url():
    url = url_entry.get().strip()
    if not url.startswith("http"):
        url = "http://" + url

    progress_bar.start()
    threading.Thread(target=asyncio.run, args=(analyze_url_async(url, progress_callback=update_progress),)).start()

def update_progress(progress):
    progress_bar['value'] = progress
    if progress == 100:
        progress_bar.stop()

def main():
    global url_entry, progress_bar

    root = tk.Tk()
    root.title("SEO Analyzer Tool")

    # ثابت کردن اندازه پنجره
    root.geometry("600x400")  # ثابت کردن اندازه پنجره به 600x400
    root.resizable(False, False)  # جلوگیری از تغییر اندازه پنجره

    # Set dark theme for the application
    root.configure(bg='black')

    frame = tk.Frame(root, padx=10, pady=10, bg='black')
    frame.pack()

    tk.Label(frame, text="Enter the website URL:", bg='black', fg='white').grid(row=0, column=0, sticky=tk.W)

    url_entry = tk.Entry(frame, width=50)
    url_entry.grid(row=0, column=1, padx=5, pady=5)

    # قرار دادن دکمه‌ها در یک خط
    button_frame = tk.Frame(root, bg='black')
    button_frame.pack(pady=10)

    analyze_button = tk.Button(button_frame, text="Analyze", command=analyze_url)
    analyze_button.pack(side=tk.LEFT, padx=10)

    save_button = tk.Button(button_frame, text="Save Report", command=lambda: save_report(results))
    save_button.pack(side=tk.LEFT, padx=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")  # اصلاح استفاده از Progressbar
    progress_bar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
