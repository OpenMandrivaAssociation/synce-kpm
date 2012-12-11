%define svn	0
%define rel	1
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
Version:	0.15
Release:	%{release} 
Source0:	http://downloads.sourceforge.net/synce/%{distname}
URL:		http://www.synce.org/moin/SynceTools/SynceKpm
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPLv2+
BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	imagemagick
# It's not actually a KDE app so it has no KDE buildrequires, but
# it only makes sense to autostart it in KDE 3, so I want to use
# %_kde3_datadir macro, which is is in kde3-macros... - AdamW 2008/09
#BuildRequires:	kde3-macros
Requires:	python-qt4
Requires:	synce-hal
Requires:	librapi-python
Requires:	python-pkg-resources
Obsoletes:	synce-kde < %{version}-%{release}
Obsoletes:	syncekonnector < %{version}-%{release}
Provides:	synce-kde = %{version}-%{release}

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
Comment=KDE panel applet and management tool for Windows Mobile devices
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Qt;TelephonyTools;Utility;
EOF

# autostart (KDE only)
#mkdir -p %{buildroot}%{_kde3_datadir}/autostart
#cat > %{buildroot}%{_kde3_datadir}/autostart/mandriva-%{name}.desktop << EOF
#[Desktop Entry]
#Exec=%{_bindir}/%{name} -i
#Icon=%{name}
#Name=SynCE panel monitor
#Terminal=false
#Type=Application
#StartupNotify=false
#OnlyShowIn=KDE;
#X-KDE-autostart-phase=2
#X-KDE-autostart-after=panel
#EOF

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%{_bindir}/%{name}
%{py_puresitedir}/synceKPM
%{py_puresitedir}/synce_kpm-%{version}-py%{pyver}.egg-info
#%{_kde3_datadir}/autostart/mandriva-%{name}.desktop
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*



%changelog
* Tue Apr 27 2010 Emmanuel Andry <eandry@mandriva.org> 0.15-1mdv2010.1
+ Revision: 539671
- New version 0.15

* Fri Aug 07 2009 Emmanuel Andry <eandry@mandriva.org> 0.14-1mdv2010.0
+ Revision: 411239
- New version 0.14
- disable kde3 autostart (TODO : migrate to kde4)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sat Nov 29 2008 Adam Williamson <awilliamson@mandriva.org> 0.12-3mdv2009.1
+ Revision: 308109
- require python-pkg-resources not python-setuptools

* Thu Sep 18 2008 Adam Williamson <awilliamson@mandriva.org> 0.12-2mdv2009.0
+ Revision: 285743
- br kde3-macros
- only have one autostart entry, for (hopefully) KDE 3: synce-trayicon can
  now handle everything for GNOME

* Wed Jul 16 2008 Adam Williamson <awilliamson@mandriva.org> 0.12-1mdv2009.0
+ Revision: 236586
- version the obsoletes and provides
- provide synce-kde
- obsolete old synce-kde components
- drop kpm-hal.diff (merged upstream)
- new release 0.12

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Jun 03 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-2mdv2009.0
+ Revision: 214455
- add kpm-hal.diff from synce-hal: support for synce-hal

* Wed Apr 16 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-1mdv2009.0
+ Revision: 194482
- new release 0.11.1

* Mon Mar 31 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3340.2mdv2008.1
+ Revision: 191329
- make menu location more consistent with similar tools (Fabrice, #39150)

* Mon Mar 24 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3340.1mdv2008.1
+ Revision: 189816
- bump to SVN 3340: don't display splash screen when starting iconified

* Mon Mar 24 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3339.1mdv2008.1
+ Revision: 189779
- update to SVN 3339 (further improvements in the rewrite)

* Sun Mar 23 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3333.1mdv2008.1
+ Revision: 189678
- adjust file lists and icon installation logic
- start iconified when autostarting
- new SVN snapshot 3333: rewrite which improves reliability, hotplugging, and allows iconified startup (all needed by us)

* Fri Mar 21 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3309.7mdv2008.1
+ Revision: 189325
- better icon (#39068, thanks Fabrice)

* Sun Mar 16 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3309.6mdv2008.1
+ Revision: 188202
- fix typo in menu entry and make it cross-desktop (thanks Fabrice F.)

* Sun Mar 16 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3309.5mdv2008.1
+ Revision: 188123
- add a menu entry

* Thu Mar 13 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3309.4mdv2008.1
+ Revision: 187393
- need to put the autostart file in /usr/share/autostart too, apparently, for KDE to find it...
- requires python-setuptools (thanks Andres)

* Wed Mar 12 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3309.2mdv2008.1
+ Revision: 187260
- add an XDG autostart file so it will be run automatically on session start

* Wed Mar 12 2008 Adam Williamson <awilliamson@mandriva.org> 0.11.1-0.3309.1mdv2008.1
+ Revision: 187234
- import synce-kpm


