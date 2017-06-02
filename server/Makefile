MARKDOWN = pandoc --from markdown_github --to html --standalone

index.html: index.md
	$(MARKDOWN) $< --output $@

setup: postgrest

postgrest: postgrest-0.4.1.0-ubuntu.tar.xz
	tar xf postgrest-0.4.1.0-ubuntu.tar.xz	

postgrest-0.4.1.0-ubuntu.tar.xz:
	wget https://github.com/begriffs/postgrest/releases/download/v0.4.1.0/postgrest-0.4.1.0-ubuntu.tar.xz

