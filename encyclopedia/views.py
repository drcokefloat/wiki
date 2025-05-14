from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry_content = util.get_entry(title)

    if entry_content is None:
        return render(request, "encyclopedia/404.html", {
            "title": title
        })

    # Convert Markdown to HTML before passing to template
    html_content = markdown2.markdown(entry_content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })


def search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return redirect('index')

    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    if len(matching_entries) == 1 and matching_entries[0].lower() == query.lower():
        # Redirect to the exact match
        return redirect('entry', title=matching_entries[0])
    else:
        # Render the search results page
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": matching_entries
        })


def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        print(f"Title: {title}")  # Debugging line
        print(f"Content: {content}")  # Debugging line

        if not title or not content:
            return render(request, "encyclopedia/create.html", {
                "error": "Title and content cannot be empty."
            })

        # Check if the entry already exists
        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            return render(request, "encyclopedia/create.html", {
                "error": f"An entry with the title '{title}' already exists."
            })

        # Save the new entry
        util.save_entry(title, content)
        return redirect('entry', title=title)

    return render(request, "encyclopedia/create.html")


