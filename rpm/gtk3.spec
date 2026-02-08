Name:           gtk3
Version:        3.24.43
Release:        1
Summary:        GTK+ 3 (Wayland-only build)

License:        LGPL-2.0-or-later
URL:            https://www.gtk.org/
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  pkgconfig
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(python3)
BuildRequires:  desktop-file-utils
BuildRequires:  shared-mime-info

# Core GNOME deps
BuildRequires:  pkgconfig(glib-2.0) >= 2.56
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(cairo) >= 1.14
BuildRequires:  pkgconfig(pango) >= 1.44
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.30
BuildRequires:  pkgconfig(tracker-sparql-3.0)
BuildRequires:  pkgconfig(atk)

# Wayland + input
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

# GL/EGL plumbing
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)

# Font stack
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(fribidi)

# Introspection disabled for now
#BuildRequires:  pkgconfig(gobject-introspection-1.0)

%description
GTK+ 3 is a toolkit for creating graphical user interfaces.
This build enables the Wayland backend and disables X11 support.

%package tools
Summary:        Utilities for GTK+ 3
Requires:       %{name} = %{version}-%{release}
%description tools
Helper utilities such as gtk-builder-tool and gtk-query-settings.

%package devel
Summary:        Development files for GTK+ 3 (Wayland-only)
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
%description devel
Headers and development files for GTK+ 3.

%prep
%autosetup -n %{name}-%{version}/upstream

%build
%meson \
  --buildtype=release \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  -Dgtk_doc=false \
  -Dman=false \
  -Dtests=false \
  -Ddemos=false \
  -Dbroadway_backend=false \
  -Dwayland_backend=true \
  -Dx11_backend=false \
  -Dtracker3=true \
  -Dintrospection=false

%meson_build

%install
%meson_install

# Don’t ship static libs
find %{buildroot}%{_libdir} -name "*.a" -delete || true

# Split translations (GTK has two domains: gtk30 and gtk30-properties)
%find_lang gtk30
%find_lang gtk30-properties
cat gtk30.lang gtk30-properties.lang > gtk30-all.lang

%post
if [ -x %{_bindir}/glib-compile-schemas ] && [ -d %{_datadir}/glib-2.0/schemas ]; then
  %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas >/dev/null 2>&1 || :
fi
if [ -x %{_bindir}/gtk-query-immodules-3.0 ]; then
  %{_bindir}/gtk-query-immodules-3.0 --update-cache >/dev/null 2>&1 || :
fi

%postun
if [ -x %{_bindir}/glib-compile-schemas ] && [ -d %{_datadir}/glib-2.0/schemas ]; then
  %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas >/dev/null 2>&1 || :
fi
if [ -x %{_bindir}/gtk-query-immodules-3.0 ]; then
  %{_bindir}/gtk-query-immodules-3.0 --update-cache >/dev/null 2>&1 || :
fi

%files -f gtk30-all.lang
%license COPYING*
%doc NEWS* README*

# Core runtime utilities
%{_bindir}/gtk-encode-symbolic-svg
%{_bindir}/gtk-launch
%{_bindir}/gtk-query-immodules-3.0
%{_bindir}/gtk-update-icon-cache

# Libraries
%{_libdir}/libgtk-3.so.*
%{_libdir}/libgdk-3.so.*
%{_libdir}/gtk-3.0

# Data
%{_datadir}/gtk-3.0
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%config(noreplace) %{_sysconfdir}/gtk-3.0/im-multipress.conf

# Keybinding themes
%{_datadir}/themes/Default/gtk-3.0/gtk-keys.css
%{_datadir}/themes/Emacs/gtk-3.0/gtk-keys.css

%files tools
%{_bindir}/gtk-builder-tool
%{_bindir}/gtk-query-settings

%files devel
%{_includedir}/gtk-3.0
%{_includedir}/gail-3.0

%{_libdir}/libgtk-3.so
%{_libdir}/libgdk-3.so
%{_libdir}/libgailutil-3.so*

%{_libdir}/pkgconfig/gtk+-3.0.pc
%{_libdir}/pkgconfig/gdk-3.0.pc
%{_libdir}/pkgconfig/gtk+-unix-print-3.0.pc
%{_libdir}/pkgconfig/gail-3.0.pc
%{_libdir}/pkgconfig/gtk+-wayland-3.0.pc
%{_libdir}/pkgconfig/gdk-wayland-3.0.pc

%{_datadir}/aclocal/gtk-3.0.m4
%{_datadir}/gettext/its/gtkbuilder.its
%{_datadir}/gettext/its/gtkbuilder.loc

