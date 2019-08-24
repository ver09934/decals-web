from django.conf.urls import url

from map import views
from map import cats
from map import cutouts

survey_regex = r'([\w +-]+)'


urlpatterns = [

    url(r'^urls', views.urls),

    url(r'^gfas', views.gfas),
    url(r'^ci', views.ci),

    #url(r'^ls-dr56/(\d+)/(\d+)/(\d+)/(\d+).jpg',
    #    views.get_tile_view('ls-dr56')),
    url(r'^ls-dr67/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('ls-dr67')),

    # 2MASS
    url(r'^2mass/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('2mass')),

    # Galex
    url(r'^galex/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('galex')),

    # PHAT M31
    url(r'^phat/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('phat')),

    url(r'^m33/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('m33')),

    # PHAT cluster catalog
    url(r'^phat-clusters/(\d+)/cat.json', cats.cat_phat_clusters),

    # eboss special DR5+ reduction
    url(r'^eboss/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('eboss')),

    # DES DR1
    url(r'^des-dr1/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('des-dr1')),

    # # MzLS+BASS DR8 tiles
    # url(r'^mzls\+bass-dr8/(\d+)/(\d+)/(\d+)/(\d+).jpg',
    #     views.get_tile_view('mzls+bass-dr8')),
    # url(r'^mzls\+bass-dr8-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
    #     views.get_tile_view('mzls+bass-dr8-model')),
    # url(r'^mzls\+bass-dr8-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
    #     views.get_tile_view('mzls+bass-dr8-resid')),
    # # DR8 catalog
    # url(r'^mzls\+bass-dr8/(\d+)/(\d+)/(\d+)/(\d+).cat.json', cats.cat_mobo_dr8),

    # DR8
    url(r'^dr8/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('dr8')),
    url(r'^dr8-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('dr8-model')),
    url(r'^dr8-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('dr8-resid')),
    url(r'^dr8/(\d+)/(\d+)/(\d+)/(\d+).cat.json', cats.cat_dr8),

    # DR8-north
    url(r'^dr8-north/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('dr8-north')),
    url(r'^dr8-north-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('dr8-north-model')),
    url(r'^dr8-north-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('dr8-north-resid')),
    url(r'^dr8-north/(\d+)/(\d+)/(\d+)/(\d+).cat.json', cats.cat_dr8_north),

    # DR8-south
    url(r'^dr8-south/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('dr8-south')),
    url(r'^dr8-south-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('dr8-south-model')),
    url(r'^dr8-south-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('dr8-south-resid')),
    url(r'^dr8-south/(\d+)/(\d+)/(\d+)/(\d+).cat.json', cats.cat_dr8_south),

    # DR7
    url(r'^decals-dr7/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decals-dr7')),
    url(r'^decals-dr7-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decals-dr7-model')),
    url(r'^decals-dr7-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decals-dr7-resid')),
    # DR7 catalog
    url(r'^decals-dr7/(\d+)/(\d+)/(\d+)/(\d+).cat.json', cats.cat_decals_dr7),

    # MzLS+BASS DR6 tiles
    url(r'^mzls\+bass-dr6/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('mzls+bass-dr6')),
    url(r'^mzls\+bass-dr6-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('mzls+bass-dr6-model')),
    url(r'^mzls\+bass-dr6-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('mzls+bass-dr6-resid')),
    # DR6 catalog
    url(r'^mzls\+bass-dr6/(\d+)/(\d+)/(\d+)/(\d+).cat.json', cats.cat_mobo_dr6),

    # DR5
    url(r'^decals-dr5/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decals-dr5')),
    url(r'^decals-dr5-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decals-dr5-model')),
    url(r'^decals-dr5-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decals-dr5-resid')),
    # DR5 catalog
    url(r'^decals-dr5/(\d+)/(\d+)/(\d+)/(\d+).cat.json', cats.cat_decals_dr5),

    # MzLS+BASS DR4 tiles
    url(r'^mzls\+bass-dr4/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('mzls+bass-dr4')),
    url(r'^mzls\+bass-dr4-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('mzls+bass-dr4-model')),
    url(r'^mzls\+bass-dr4-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('mzls+bass-dr4-resid')),
    # DR4 catalog
    url(r'^mzls\+bass-dr4/(\d+)/(\d+)/(\d+)/(\d+).cat.json', cats.cat_mobo_dr4),

    # DR4/5 DESI targets
    url(r'^targets-dr45/(\d+)/cat.json', cats.cat_targets_dr45),
     # DR6/7 DESI targets
    url(r'^targets-dr67/(\d+)/cat.json', cats.cat_targets_dr67),

     # DR6/7 DESI targets, BGS survey only
    url(r'^targets-bgs-dr67/(\d+)/cat.json', cats.cat_targets_bgs_dr67),

    # DR6/7 DESI sky fibers
    url(r'^targets-sky-dr67/(\d+)/cat.json', cats.cat_targets_sky_dr67),

    url(r'^targets-dark-dr67/(\d+)/cat.json', cats.cat_targets_dark_dr67),
    url(r'^targets-bright-dr67/(\d+)/cat.json', cats.cat_targets_bright_dr67),

    url(r'^targets-cmx-dr7/(\d+)/cat.json', cats.cat_targets_cmx_dr7),

    # DR8
    url(r'^targets-dr8/(\d+)/cat.json', cats.cat_targets_dr8),
    url(r'^targets-sv-dr8/(\d+)/cat.json', cats.cat_targets_sv_dr8),

    # DECaPS2 tiles
    url(r'^decaps2/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decaps2')),
    url(r'^decaps2-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decaps2-model')),
    url(r'^decaps2-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decaps2-resid')),
    # aka DECaPS
    url(r'^decaps/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decaps2')),
    url(r'^decaps-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decaps2-model')),
    url(r'^decaps-resid/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('decaps2-resid')),
    
    # Gaia catalog
    url(r'^gaia-dr1/(\d+)/cat.json', cats.cat_gaia_dr1),
    url(r'^gaia-dr2/(\d+)/cat.json', cats.cat_gaia_dr2),

    # Upload user catalog
    url(r'^upload-cat/', cats.upload_cat, name='upload-cat'),

    # AJAX retrieval of user catalogs
    url(r'^usercatalog/(\d+)/cat.json', cats.cat_user),

    # DEEP2 Spectroscopy catalog
    url(r'^spec-deep2/(\d+)/cat.json', cats.cat_spec_deep2),

    # SDSS Catalog
    url(r'^sdss-cat/(\d+)/cat.json', cats.cat_sdss),

    # SDSS tiled coadd
    url(r'^sdssco/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('sdssco')),

    url(r'^sdss2/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('sdss2')),
    
    # PS1 skycells
    url(r'^ps1/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('ps1')),
    # PS1 catalog test
    url(r'^ps1/(\d+)/cat.json', cats.cat_ps1),

    # HSC
    url(r'^hsc/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('hsc')),

    url(r'^vlass/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('vlass')),

    # For nova.astrometry.net: SDSS for a given WCS
    url(r'^sdss-wcs', views.sdss_wcs),

    # Used by the CI image viewer: render image into given WCS
    # (eg http://legacysurvey.org/viewer-dev/ci?ra=195&dec=60)
    url(r'^cutout-wcs', views.cutout_wcs),

    url(r'^data-for-radec/', views.data_for_radec, name='data_for_radec'),

    url(r'^namequery/', views.name_query, name='object-query'),

    # CCDs: list of polygons
    url(r'^ccds/', views.ccd_list, name='ccd-list'),
    # Exposures: list of circles
    url(r'^exps/', views.exposure_list, name='exposure-list'),

    # Tycho-2 stars
    url(r'^tycho2/(\d+)/cat.json', cats.cat_tycho2),

    # Cutouts
    #url(r'^jpeg-cutout', cutouts.jpeg_cutout, name='cutout-jpeg'),
    #url(r'^fits-cutout', cutouts.fits_cutout, name='cutout-fits'),
    url(r'^cutout.jpg', cutouts.jpeg_cutout, name='cutout-jpeg'),
    url(r'^cutout.fits', cutouts.fits_cutout, name='cutout-fits'),
    url(r'^jpeg-cutout', cutouts.jpeg_cutout),
    url(r'^fits-cutout', cutouts.fits_cutout),


    # NGC/IC/UGC galaxies
    url(r'^ngc/(\d+)/cat.json', cats.cat_gals),

    # LSLGA galaxies
    url(r'^lslga/(\d+)/cat.json', cats.cat_lslga),
    
    # Virgo cluster catalog (VCC) objects
    #url(r'^vcc/(\d+)/cat.json', views.cat_vcc),

    # SDSS Spectroscopy
    url(r'^spec/(\d+)/cat.json', cats.cat_spec),

    # Bright stars
    url(r'^bright/(\d+)/cat.json', cats.cat_bright),

    # SFD dust map
    url(r'^sfd/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('sfd')),

    # WSSA WISE 12-micron dust map
    url(r'^wssa/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('wssa')),

    # Halpha map
    url(r'^halpha/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('halpha')),

    # Original unWISE W1/W2
    url(r'^unwise-w1w2/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('unwise-w1w2')),
    # Aaron's NEOx unWISE W1/W2
    # NEO2
    url(r'^unwise-neo2/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('unwise-neo2')),
    # NEO3
    url(r'^unwise-neo3/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('unwise-neo3')),
    # NEO4
    url(r'^unwise-neo4/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('unwise-neo4')),
    # unWISE catalog model
    url(r'^unwise-cat-model/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.get_tile_view('unwise-cat-model')),

    #url(r'^unwise-w3w4-tiles/(\d+)/(\d+)/(\d+)/(\d+).jpg', views.map_unwise_w3w4),


    # DR8 tests -- generic layers
    url(r'^([\w\+-]+)/(\d+)/(\d+)/(\d+)/(\d+).jpg',
        views.any_tile_view),
    # catalog
    url(r'^([\w\+-]+)/(\d+)/(\d+)/(\d+)/(\d+).cat.json',
        cats.any_cat),


    # Cutouts html
    url(r'^cutouts/', views.cutouts, name='cutouts'),
    # Cutouts panel plots
    url(r'^cutout_panels/(?P<layer>.*)/(?P<expnum>\d+)/(?P<extname>\w+)/', views.cutout_panels, name='cutout_panels'),
    # Scatterplot of nearby sources for cutouts page
    #url(r'^cat_plot/', views.cat_plot, name='cat_plot'),

    # PSF for a single expnum/ccdname -- half-finished.
    #url(r'^cutout_psf/(?P<layer>.*)/(?P<expnum>\d+)/(?P<extname>\w+)/', views.cutout_psf,
    #name='cutout_psf'),

    url(r'^cutouts-tgz/', views.cutouts_tgz, name='cutouts_tgz'),

    url(r'^coadd-psf/', views.cutouts_coadd_psf, name='coadd_psf'),

    # Look up this position, date, observatory in JPL Small Bodies database
    url(r'^jpl_lookup/', views.jpl_lookup),

    # bricks: list of polygons
    url(r'^bricks/', views.brick_list, name='brick-list'),

    # SDSS spectro plates: list of circles
    url(r'^sdss-plates/', views.sdss_plate_list, name='sdss-plate-list'),

    # Brick details
    url(r'^brick/(\d{4}[pm]\d{3})', views.brick_detail, name='brick_detail'),
    # this one is here to provide a name for the javascript to refer to.
    url(r'^brick/', views.nil, name='brick_detail_blank'),
    # CCD details
    url(r'^ccd/%s/([\w-]+)' % survey_regex, views.ccd_detail, name='ccd_detail'),
    # this one is here to provide a name for the javascript to refer to.
    url(r'^ccd/', views.nil, name='ccd_detail_blank'),
    # Exposure details
    url(r'^exposure/([\w-]+)/([\w-]+)', views.exposure_detail, name='exp_detail'),
    # this one is here to provide a name for the javascript to refer to.
    url(r'^exposure/', views.nil, name='exp_detail_blank'),

    # Image data
    url(r'^image-data/%s/([\w-]+)' % survey_regex, views.image_data, name='image_data'),
    url(r'^dq-data/%s/([\w-]+)' % survey_regex, views.dq_data, name='dq_data'),
    url(r'^iv-data/%s/([\w-]+)' % survey_regex, views.iv_data, name='iv_data'),

    url(r'^image-stamp/%s/([\w-]+).jpg' % survey_regex, views.image_stamp, name='image_stamp'),

    # Special DECaPS version of viewer.
    url(r'decaps', views.decaps),

    # Special M33 version of viewer.
    url(r'm33', views.m33),

    # DR5 version of the viewer.
    url(r'dr5', views.dr5),
    # DR6 version of the viewer.
    url(r'dr6', views.dr6),

    # PHAT version of the viewer.
    url(r'^phat/?$', views.phat),

    # fall-through
    url(r'', views.index),

]
