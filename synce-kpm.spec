%define svn	0
%define rel	2
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name-%svn.tar.lzma
%define dirname		%name
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.gz
%define dirname		%name-%version
%endif

Name:		synce-kpm
Summary:	Graphical tool for managing Windows Mobile devices
Version:	0.11.1
Release:	%{release} 
Source0:	http://downloads.sourceforge.net/synce/%{distname}
# From synce-hal SVN: support synce-hal - AdamW 2008/06
Patch0:		kpm-hal.diff
URL:		http://www.synce.org/moin/SynceTools/SynceKpm
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPLv2+
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	ImageMagick
Requires:	python-qt4
Requires:	synce-hal
Requires:	librapi-python
Requires:	python-setuptools

%description
SynCE-KPM stands for SynCE KDE PDA Manager and aims to be an
application to manage WM5/WM6 PDA devices from Linux. SynCE-KPM
provides the following features for managing your WM5/WM6 PDA from the
PC:

* Install / uninstall programs
* Display general device information
* Manage partnerships

%prep
%setup -q -n %{dirname}
%patch0 -p1 -b .hal

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --root=%{buildroot} --compile --optimize=2

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16,scalable}/apps
install -m 0644 synceKPM/data/synce-green-scalable.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
convert -scale 48x48 synceKPM/data/synce-green-scalable.svg %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32x32 synceKPM/data/synce-green-scalable.svg %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16x16 synceKPM/data/synce-green-scalable.svg %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=SynCE panel monitor
Comment=Panel applet and management tool for Windows Mobile devices
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Qt;TelephonyTools;Utility;X-MandrivaLinux-CrossDesktop;
EOF

# XDG autostart
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
cat > %{buildroot}%{_sysconfdir}/xdg/autostart/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Exec=%{_bindir}/%{name} -i
Icon=%{name}
Name=SynCE panel monitor
Terminal=false
Type=Application
StartupNotify=false
X-KDE-autostart-phase=2
X-KDE-autostart-after=panel
EOF

# KDE autostart
mkdir -p %{buildroot}%{_datadir}/autostart
cp %{buildroot}%{_sysconfdir}/xdg/autostart/mandriva-%{name}.desktop %{buildroot}%{_datadir}/autostart/mandriva-%{name}.desktop

%post
%{update_menus}
%{update_icon_cache hicolor}

%postun
%{clean_menus}
%{clean_icon_cache hicolor}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%{py_puresitedir}/synceKPM
%{py_puresitedir}/synce_kpm-%{version}-py%{pyver}.egg-info
%{_sysconfdir}/xdg/autostart/mandriva-%{name}.desktop
%{_datadir}/autostart/mandriva-%{name}.desktop
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*

