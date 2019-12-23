from __future__ import print_function
import os
import sys
from glob import glob

sys.path.insert(0, 'django-1.9')
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'viewer.settings'

from viewer import settings
settings.READ_ONLY_BASEDIR = False
#settings.DEBUG_LOGGING = True

from map.views import *

from astrometry.util.multiproc import *
from astrometry.util.fits import *
from astrometry.libkd.spherematch import *

import logging
lvl = logging.DEBUG
logging.basicConfig(level=lvl, format='%(message)s', stream=sys.stdout)

class duck(object):
    pass

req = duck()
req.META = dict(HTTP_IF_MODIFIED_SINCE=None)

version = 1

def get_version(kind):
    return 1

def _one_tile(X):
    (kind, zoom, x, y, ignore, get_images) = X
    kwargs = dict(ignoreCached=ignore,
                  get_images=get_images)

    print()
    print('one_tile: zoom', zoom, 'x,y', x,y)

    # forcecache=False, return_if_not_found=True)
    if kind == 'sdss':
        print('Zoom', zoom, 'x,y', x,y)
        v = 1
        layer = get_layer('sdssco')
        return layer.get_tile(req, v, zoom, x, y, savecache=True, forcecache=True,
                              **kwargs)

    elif kind == 'sdss2':
        v = 1
        layer = get_layer(kind)
        return layer.get_tile(req, v, zoom, x, y, savecache=True, forcecache=True,
                              **kwargs)
        
    elif kind == 'ps1':
        print('Zoom', zoom, 'x,y', x,y)
        from map import views
        get_tile = views.get_tile_view('ps1')
        get_tile(req, version, zoom, x, y, savecache=True,
                 return_if_not_found=True)

    elif kind in ['decals-dr5', 'decals-dr5-model', 'decals-dr5-resid',
                  'mzls+bass-dr6', 'mzls+bass-dr6-model', 'mzls+bass-dr6-resid']:
        v = 1
        layer = get_layer(kind)
        return layer.get_tile(req, v, zoom, x, y, savecache=True, forcecache=True,
                              **kwargs)

    elif kind in ['eboss']:
        v = 1
        layer = get_layer(kind)
        return layer.get_tile(req, v, zoom, x, y, savecache=True, forcecache=True,
                              **kwargs)
        
    elif kind in ['mzls+bass-dr4', 'mzls+bass-dr4-model', 'mzls+bass-dr4-resid']:
        v = 2
        layer = get_layer(kind)
        return layer.get_tile(req, v, zoom, x, y, savecache=True, return_if_not_found=True, **kwargs)

    elif kind in ['decaps2', 'decaps2-model', 'decaps2-resid']:
        v = 2
        layer = get_layer(kind)
        print('kind', kind, 'zoom', zoom, 'x,y', x,y)
        return layer.get_tile(req, v, zoom, x, y, savecache=True, forcecache=True,
                              get_images=get_images, ignoreCached=True)
        
    elif kind in ['decals-dr3', 'decals-dr3-model', 'decals-dr3-resid']:
        v = 1
        layer = get_layer(kind)
        layer.get_tile(req, v, zoom, x, y, savecache=True, forcecache=True)

    elif kind in ['decals-dr2', 'decals-dr2-model', 'decals-dr2-resid']:
        v = 2
        kwa = {}
        if 'model' in kind:
            v = 1
            kwa.update(model=True, add_gz=True)
        if 'resid' in kind:
            v = 1
            kwa.update(resid=True, model_gz=True)

        print('map_decals_dr2 kwargs:', kwa)
        map_decals_dr2(req, v, zoom, x, y, savecache=True, forcecache=True,
                       hack_jpeg=True, drname='decals-dr2', **kwa)

    elif kind == 'sfd':
        v = 2
        layer = sfd_layer
        layer.get_tile(req, v, zoom, x, y, savecache=True)
        #map_sfd(req, version, zoom, x, y, savecache=True)
    elif kind == 'halpha':
        map_halpha(req, version, zoom, x, y, savecache=True)

    elif kind == 'unwise':
        map_unwise_w1w2(req, version, zoom, x, y, savecache=True,
                        ignoreCached=ignore)
        print('unWISE zoom', zoom, 'x,y', x,y)

    elif kind in ['unwise-neo2', 'unwise-neo3']:
        from map import views
        view = views.get_tile_view(kind)
        return view(req, version, zoom, x, y, savecache=True, **kwargs)

    else:
        from map import views
        view = views.get_tile_view(kind)
        return view(req, version, zoom, x, y, savecache=True, **kwargs)

def _bounce_one_tile(*args):
    try:
        _one_tile(*args)
    except KeyboardInterrupt:
        raise
    except:
        print('Error in _one_tile(', args, '):')
        import traceback
        traceback.print_exc()

def _bounce_map_unwise_w1w2(args):
    return map_unwise_w1w2(*args, ignoreCached=True, get_images=True)
def _bounce_map_unwise_w3w4(args):
    return map_unwise_w3w4(*args, ignoreCached=True, get_images=True)

def _bounce_sdssco(X):
    (args,kwargs) = X
    (req,ver,zoom,x,y) = args
    fn = 'top-sdss-%i-%i-%i.fits' % (zoom, x, y)
    save = False
    if os.path.exists(fn):
        img = fitsio.read(fn)
        print('Read', img.shape)
        H,W,planes = img.shape
        ims = [img[:,:,i] for i in range(planes)]
    else:
        #ims = map_sdss(*args, ignoreCached=True, get_images=True, **kwargs)
        ims = map_sdssco(*args, ignoreCached=True, get_images=True, 
                          hack_jpeg=True, **kwargs)
        if ims is None:
            return ims
        save = True

    # Save jpeg
    #tag = 'sdss'
    tag = 'sdssco'
    pat = os.path.join(settings.DATA_DIR, 'tiles', tag, '%(ver)s',
                       '%(zoom)i', '%(x)i', '%(y)i.jpg')
    tilefn = pat % dict(ver=1, zoom=zoom, x=x, y=y)
    if not os.path.exists(tilefn):
        bands = 'gri'
        rgb = sdss_rgb(ims, bands)
        trymakedirs(tilefn)
        save_jpeg(tilefn, rgb)
        print('Wrote', tilefn)

    # Save FITS
    if save:
        d = np.dstack(ims)
        print('writing', d.shape, 'to', fn)
        fitsio.write(fn, d, clobber=True)

    return ims

def _bounce_decals_dr3(X):
    (args,kwargs) = X
    print('Bounce_decals_dr3: kwargs', kwargs)
    tag = 'image'
    if 'model' in kwargs:
        tag = 'model'
    if 'resid' in kwargs:
        tag = 'resid'
    (req,ver,zoom,x,y) = args
    print('Tag', tag)
    fn = 'top-dr3-%s-%i-%i-%i.fits' % (tag, zoom, x, y)
    if os.path.exists(fn):
        img = fitsio.read(fn)
        print('Read', img.shape)
        H,W,planes = img.shape
        ims = [img[:,:,i] for i in range(planes)]
        return ims

    ims = map_decals_dr3(*args, ignoreCached=True, get_images=True, write_jpeg=True,
                          hack_jpeg=True, forcecache=True, **kwargs)
    if ims is None:
        return ims
    # save FITS
    d = np.dstack(ims)
    print('writing', d.shape, 'to', fn)
    fitsio.write(fn, d, clobber=True)

    return ims

def top_levels(mp, opt):
    from map.views import save_jpeg, trymakedirs

    if opt.kind in ['decaps2', 'decaps2-model', 'decaps2-resid',
                    'mzls+bass-dr4', 'mzls+bass-dr4-model', 'mzls+bass-dr4-resid',
                    'decals-dr5', 'decals-dr5-model', 'decals-dr5-resid',
                    'decals-dr7', 'decals-dr7-model', 'decals-dr7-resid',
                    'mzls+bass-dr6', 'mzls+bass-dr6-model', 'mzls+bass-dr6-resid',
                    'des-dr1',
                    'eboss',
                    'unwise-neo2', 'unwise-neo3', 'unwise-neo4', 'unwise-cat-model',
                    'galex', 'sdss2', 'wssa',
                    'ls-dr56', 'ls-dr67'] or True:
        import pylab as plt
        from viewer import settings
        import fitsio
        from scipy.ndimage.filters import gaussian_filter
        from map.views import _unwise_to_rgb
        tag = opt.kind

        from map.views import get_layer
        layer = get_layer(opt.kind)

        bands = layer.get_bands()

        print('Layer:', layer)
        #print('Survey:', layer.survey)
        #print('  cache_dir:', layer.survey.cache_dir)

        print('Bands', bands)

        rgbkwargs = {}
        if opt.kind in ['unwise-neo2', 'unwise-neo3', 'unwise-neo4', 'unwise-cat-model']:
            bands = [1, 2]
        elif opt.kind == 'sdss2':
            bands = 'gri'
        elif opt.kind == 'galex':
            bands = ['n','f']
        elif opt.kind == 'wssa':
            bands = ['x']
        #else:
        #    bands = 'grz'

        ver = tileversions.get(opt.kind, [1])[-1]
        print('Version', ver)
        basescale = 5

        pat = os.path.join(settings.DATA_DIR, 'tiles', tag, '%(ver)s',
                           '%(zoom)i', '%(x)i', '%(y)i.jpg')
        patdata = dict(ver=ver)

        tilesize = 256
        tiles = 2**basescale
        side = tiles * tilesize

        basepat = 'base-%s-%i-%%s.fits' % (opt.kind, basescale)

        basefns = [basepat % band for band in bands]
        if not all([os.path.exists(fn) for fn in basefns]):
            bases = [np.zeros((side, side), np.float32) for band in bands]

            args = []
            xy = []
            if opt.y1 is None:
                opt.y1 = tiles
            if opt.x0 is None:
                opt.x0 = 0
            if opt.x1 is None:
                opt.x1 = tiles
            for y in range(opt.y0, opt.y1):
                for x in range(opt.x0, opt.x1):
                    args.append((opt.kind, basescale, x, y, False, True))
                    xy.append((x,y))

            tiles = mp.map(_one_tile, args)

            for ims,(x,y) in zip(tiles, xy):

                #for a,(x,y) in zip(args, xy):
                #print('_one_tile args:', a)
                #ims = _one_tile(a)
                #print('-> ', ims)

                if ims is None:
                    continue
                for im,base in zip(ims, bases):
                    if im is None:
                        continue
                    base[y*tilesize:(y+1)*tilesize,
                         x*tilesize:(x+1)*tilesize] = im

            for fn,base in zip(basefns, bases):
                fitsio.write(fn, base, clobber=True)
        else:
            print('Reading', basefns)
            bases = [fitsio.read(fn) for fn in basefns]

        for scale in range(basescale, -1, -1):
            print('Scale', scale)
            tiles = 2**scale
            for y in range(tiles):
                for x in range(tiles):
                    ims = [base[y*tilesize:(y+1)*tilesize,
                                x*tilesize:(x+1)*tilesize] for base in bases]
                    rgb = layer.get_rgb(ims, bands, **rgbkwargs)
                    pp = patdata.copy()
                    pp.update(zoom=scale, x=x, y=y)
                    fn = pat % pp
                    trymakedirs(fn)
                    save_jpeg(fn, rgb)
                    print('Wrote', fn)

            for i,base in enumerate(bases):
                if 'vlass' in opt.kind:
                    base = np.maximum(np.maximum(base[::2,::2], base[1::2,::2]),
                                      np.maximum(base[1::2,1::2], base[::2,1::2]))
                else:
                    base = (base[::2,::2] + base[1::2,::2] + base[1::2,1::2] + base[::2,1::2])/4.
                bases[i] = base


    elif opt.kind in ['unwise', 'unwise-neo1', 'unwise-w3w4',]:
        import pylab as plt
        from viewer import settings
        from map.views import _unwise_to_rgb
        import fitsio

        if opt.kind == 'unwise-w3w4':
            tag = 'unwise-w3w4'
            bands = [3,4]
            bounce = _bounce_map_unwise_w3w4
        elif opt.kind == 'unwise-neo1':
            tag = 'unwise-neo1'
            bands = [1,2]
            bounce = _bounce_map_unwise_neo1
        else:
            tag = 'unwise-w1w2'
            bands = [1,2]
            bounce = _bounce_map_unwise_w1w2

        pat = os.path.join(settings.DATA_DIR, 'tiles', tag, '%(ver)s',
                           '%(zoom)i', '%(x)i', '%(y)i.jpg')
        ver = 1
        patdata = dict(ver=ver)

        basescale = 4

        tilesize = 256
        tiles = 2**basescale
        side = tiles * tilesize

        basepat = 'base-%s-%i-%%s.fits' % (opt.kind, basescale)
        basefns = [basepat % band for band in bands]

        if not all([os.path.exists(fn) for fn in basefns]):
            bases = [np.zeros((side, side), np.float32) for band in bands]

            args = []
            for y in range(tiles):
                for x in range(tiles):
                    #print 'Base tile', x, y
                    args.append((req, ver, basescale, x, y))
            tiles = mp.map(bounce, args)
            for ims,arg in zip(tiles,args):
                x,y = arg[-2:]
                for im,base in zip(ims, bases):
                    if im is None:
                        continue
                    base[y*tilesize:(y+1)*tilesize,
                         x*tilesize:(x+1)*tilesize] = im

            for fn,base in zip(basefns, bases):
                fitsio.write(fn, base, clobber=True)
        else:
            print('Reading', basefns)
            bases = [fitsio.read(fn) for fn in basefns]

            if False:
                # Messin' around
                plt.figure(figsize=(8,8))
                plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
                #for S in [1000, 3000, 10000]:
                #for Q in [10, 25, 50]:
                S,Q = 3000,25
                im = _unwise_to_rgb([w1base, w2base], S=S, Q=Q)
                #plt.clf()
                #plt.imshow(im)
                plt.imsave('base-S%i-Q%s.png' % (S,Q), im)

                # Try converting to galactic coords...
                from astrometry.util.util import anwcs_create_mercator_2

                print('Base images:', w1base.shape)
                zoom = basescale
                h,w = w1base.shape
                zoomscale = 2.**zoom * (256./h)
                print('Zoomscale', zoomscale)
                wcs = anwcs_create_mercator_2(180., 0., w/2., h/2.,
                                              zoomscale, w, h, 1)

                wcs2 = anwcs_create_mercator_2(0., 0., w/2., h/2.,
                                               zoomscale, w, h, 1)

                print('WCS:')
                for x,y in [(1,1), (1,h), (w,1), (w,h), (w/2,1), (w/2,h/2)]:
                    print('x,y', (x,y), '-> RA,Dec', wcs.pixelxy2radec(x,y)[-2:])

                ok,ras,nil  = wcs2.pixelxy2radec(np.arange(w), np.ones(w))
                ok,nil,decs = wcs2.pixelxy2radec(np.ones(h), np.arange(h))
                print('RAs', ras.shape)
                print('Decs', decs.shape)

                lls = ras
                bbs = decs

                ll,bb = np.meshgrid(lls, bbs)
                print('LL,BB', ll.shape, bb.shape)

                from astrometry.util.starutil_numpy import lbtoradec

                ra,dec = lbtoradec(ll,bb)
                print('RA,Dec', ra.shape, dec.shape)

                ok,xx,yy = wcs.radec2pixelxy(ra, dec)
                print('xx,yy', xx.shape, yy.shape)

                lb1 = w1base[np.clip(np.round(yy-1).astype(int), 0, h-1),
                             np.clip(np.round(xx-1).astype(int), 0, w-1)]
                lb2 = w2base[np.clip(np.round(yy-1).astype(int), 0, h-1),
                             np.clip(np.round(xx-1).astype(int), 0, w-1)]

                lbim = _unwise_to_rgb(lb1, lb2, S=S,Q=Q)
                plt.imsave('lb.png', lbim)

                sys.exit(0)

        from scipy.ndimage.filters import gaussian_filter

        for scale in range(basescale-1, -1, -1):

            for i,base in enumerate(bases):
                base = gaussian_filter(base, 1.)
                base = (base[::2,::2] + base[1::2,::2] + base[1::2,1::2] + base[::2,1::2])/4.
                bases[i] = base

            tiles = 2**scale
            
            for y in range(tiles):
                for x in range(tiles):
                    ims = [base[y*tilesize:(y+1)*tilesize,
                                x*tilesize:(x+1)*tilesize] for base in bases]
                    tile = _unwise_to_rgb(ims, bands=bands)
                    pp = patdata.copy()
                    pp.update(zoom=scale, x=x, y=y)
                    fn = pat % pp
                    trymakedirs(fn)
                    save_jpeg(fn, tile)
                    print('Wrote', fn)


    if opt.kind in ['depth-g', 'depth-r', 'depth-z']:
        import pylab as plt
        from viewer import settings
        from scipy.ndimage.filters import gaussian_filter
        from map.views import trymakedirs

        tag = 'decam-' + opt.kind
        #band = opt.kind[-1]
        ver = 1
        basescale = 5
        pat = os.path.join(settings.DATA_DIR, 'tiles', tag, '%(ver)s',
                           '%(zoom)i', '%(x)i', '%(y)i.jpg')
        patdata = dict(ver=ver)
        tilesize = 256
        tiles = 2**basescale
        side = tiles * tilesize
        
        base = np.zeros((side, side, 3), np.float32)
        for y in range(tiles):
            for x in range(tiles):
                dat = patdata.copy()
                dat.update(zoom=basescale, x=x, y=y)
                fn = pat % dat
                if not os.path.exists(fn):
                    print('Does not exist:', fn)
                    continue
                img = plt.imread(fn)
                base[y*tilesize:(y+1)*tilesize,
                     x*tilesize:(x+1)*tilesize,:] = img

        for scale in range(basescale-1, -1, -1):

            newbase = []
            for i in range(3):
                b = gaussian_filter(base[:,:,i], 1.)
                b = (b[ ::2, ::2] + b[1::2, ::2] +
                     b[1::2,1::2] + b[ ::2,1::2])/4.
                newbase.append(b)
            base = np.dstack(newbase)

            tiles = 2**scale
            for y in range(tiles):
                for x in range(tiles):
                    img = base[y*tilesize:(y+1)*tilesize,
                               x*tilesize:(x+1)*tilesize, :]

                    pp = patdata.copy()
                    pp.update(zoom=scale, x=x, y=y)
                    fn = pat % pp
                    trymakedirs(fn)
                    plt.imsave(fn, np.clip(np.round(img).astype(np.uint8), 0, 255))
                    print('Wrote', fn)


    ### HACK... factor this out...
    if opt.kind in ['sdss',
                    'decals-dr2', 'decals-dr2-model', 'decals-dr2-resid',
                    'decals-dr3', 'decals-dr3-model', 'decals-dr3-resid',
                    ]:
        import pylab as plt
        from viewer import settings
        from legacypipe.survey import get_rgb
        import fitsio
        from scipy.ndimage.filters import gaussian_filter

        tag = opt.kind

        bouncemap = {
            'sdss': _bounce_sdssco,
            'decals-dr3': _bounce_decals_dr3,
            'decals-dr3-model': _bounce_decals_dr3,
            'decals-dr3-resid': _bounce_decals_dr3,
            }
        bounce = bouncemap[opt.kind]

        rgbkwargs = dict(mnmx=(-1,100.), arcsinh=1.)

        bands = 'grz'
        if opt.kind in ['decals-dr2', 'decals-dr2-model',
                        'decals-dr3', 'decals-dr3-model',]:
            get_rgb = dr2_rgb
            rgbkwargs = {}
        elif opt.kind == 'sdssco':
            rgbkwargs = {}

        ver = tileversions.get(opt.kind, [1])[-1]
        print('Version', ver)
        basescale = 5

        pat = os.path.join(settings.DATA_DIR, 'tiles', tag, '%(ver)s',
                           '%(zoom)i', '%(x)i', '%(y)i.jpg')
        patdata = dict(ver=ver)

        tilesize = 256
        tiles = 2**basescale
        side = tiles * tilesize

        basepat = 'base-%s-%i-%%s.fits' % (opt.kind, basescale)

        basefns = [basepat % band for band in bands]
        if not all([os.path.exists(fn) for fn in basefns]):
            bases = [np.zeros((side, side), np.float32) for band in bands]

            args = []
            kwa = dict()
            if 'model' in opt.kind:
                kwa.update(model=True, add_gz=True)
            elif 'resid' in opt.kind:
                kwa.update(resid=True, model_gz=True)

            xy = []
            if opt.y1 is None:
                opt.y1 = tiles
            if opt.x0 is None:
                opt.x0 = 0
            if opt.x1 is None:
                opt.x1 = tiles
            for y in range(opt.y0, opt.y1):
                for x in range(opt.x0, opt.x1):
                    args.append(((req, ver, basescale, x, y),kwa))
                    xy.append((x,y))
            tiles = mp.map(bounce, args)
            for ims,(x,y) in zip(tiles, xy):
                if ims is None:
                    continue
                for im,base in zip(ims, bases):
                    if im is None:
                        continue
                    base[y*tilesize:(y+1)*tilesize,
                         x*tilesize:(x+1)*tilesize] = im

            for fn,base in zip(basefns, bases):
                fitsio.write(fn, base, clobber=True)
        else:
            print('Reading', basefns)
            bases = [fitsio.read(fn) for fn in basefns]

        #for scale in range(basescale-1, -1, -1):
        for scale in range(basescale, -1, -1):
            print('Scale', scale)
            tiles = 2**scale
            for y in range(tiles):
                for x in range(tiles):
                    ims = [base[y*tilesize:(y+1)*tilesize,
                                x*tilesize:(x+1)*tilesize] for base in bases]

                    if opt.kind == 'sdss':
                        bands = 'gri'
                        rgb = sdss_rgb(ims, bands)
                    else:
                        rgb = get_rgb(ims, bands, **rgbkwargs)

                    pp = patdata.copy()
                    pp.update(zoom=scale, x=x, y=y)
                    fn = pat % pp
                    trymakedirs(fn)
                    save_jpeg(fn, rgb)
                    print('Wrote', fn)

            for i,base in enumerate(bases):
                #base = gaussian_filter(base, 1.)
                base = (base[::2,::2] + base[1::2,::2] + base[1::2,1::2] + base[::2,1::2])/4.
                bases[i] = base



def _layer_get_filename(args):
    layer,brick,band,scale,force = args

    if force:
        fn = layer.get_scaled_filename(brick, band, scale)
        if os.path.exists(fn):
            os.remove(fn)

    fn = layer.get_filename(brick, band, scale)
    print(fn)

def main():
    import optparse

    parser = optparse.OptionParser()
    parser.add_option('--zoom', '-z', type=int, action='append', default=[],
                      help='Add zoom level; default 13')
    parser.add_option('--threads', type=int, default=1, help='Number of threads')
    parser.add_option('--y0', type=int, default=0, help='Start row')
    parser.add_option('--y1', type=int, default=None, help='End row (non-inclusive)')

    parser.add_option('--x0', type=int, default=None)
    parser.add_option('--x1', type=int, default=None)

    parser.add_option('-x', type=int)
    parser.add_option('-y', type=int)

    parser.add_option('--mindec', type=float, default=None, help='Minimum Dec to run')
    parser.add_option('--maxdec', type=float, default=None, help='Maximum Dec to run')

    parser.add_option('--minra', type=float, default=None,   help='Minimum RA to run')
    parser.add_option('--maxra', type=float, default=None, help='Maximum RA to run')

    parser.add_option('--touching', default=False, action='store_true',
                      help='Select bricks touching min/max ra/dec box (vs container within)')

    parser.add_option('--near', action='store_true', help='Only run tiles near bricks')

    parser.add_option('--near-ccds', action='store_true', help='Only run tiles near CCDs')

    parser.add_option('--queue', action='store_true', default=False,
                      help='Print qdo commands')

    parser.add_option('--all', action='store_true', help='Render all tiles')

    parser.add_option('--ignore', action='store_true', help='Ignore cached tile files',
                      default=False)

    parser.add_option('--top', action='store_true', help='Top levels of the pyramid')

    parser.add_option('--split', action='store_true', help='For split layers (DR6+DR7), only compute one y strip per zoom level')

    parser.add_option('--bricks-exist', action='store_true', help='Create table of bricks that exist')

    parser.add_option('--kind', default='image')
    parser.add_option('--scale', action='store_true', help='Scale images?')
    parser.add_option('--bricks', action='store_true', help='Compute scaled brick tables?')
    parser.add_option('--coadd', action='store_true', help='Create SDSS coadd images?')
    parser.add_option('--grass', action='store_true', help='progress plot')

    parser.add_option('--bands', default=None)

    parser.add_option('-v', '--verbose', dest='verbose', action='count',
                      default=0, help='Make more verbose')


    opt,args = parser.parse_args()

    if opt.verbose == 0:
        lvl = logging.INFO
    else:
        lvl = logging.DEBUG
    logging.basicConfig(level=lvl, format='%(message)s', stream=sys.stdout)


    mp = multiproc(opt.threads)

    if opt.kind in ['sdss', 'sdss2']:
        if opt.maxdec is None:
            opt.maxdec = 90
        if opt.mindec is None:
            opt.mindec = -25
    elif opt.kind in ['halpha', 'unwise-neo1', 'unwise-neo2', 'unwise-neo3', 'unwise-neo4', 'unwise-cat-model',
                      'galex', 'wssa', 'vlass', 'hsc', 'hsc2'] or 'dr8i' in opt.kind:
        if opt.maxdec is None:
            opt.maxdec = 90.
        if opt.mindec is None:
            opt.mindec = -90.
        if opt.maxra is None:
            opt.maxra = 360.
        if opt.minra is None:
            opt.minra = 0.

        if opt.kind == 'galex' and opt.bands is None:
            opt.bands = 'nf'
        if 'unwise' in opt.kind and opt.bands is None:
            opt.bands = '12'
        if 'vlass' in opt.kind:
            opt.bands = [1]

    elif opt.kind == 'm33':
        if opt.mindec is None:
            opt.mindec = 30.40
        if opt.maxdec is None:
            opt.maxdec = 30.90
        if opt.minra is None:
            opt.minra = 23.29
        if opt.maxra is None:
            opt.maxra = 23.73

    elif opt.kind == 'm33':
        if opt.mindec is None:
            opt.mindec = 30.40
        if opt.maxdec is None:
            opt.maxdec = 30.90
        if opt.minra is None:
            opt.minra = 23.29
        if opt.maxra is None:
            opt.maxra = 23.73

    elif opt.kind in ['des-dr1']:
        if opt.maxdec is None:
            opt.maxdec = 6
        if opt.mindec is None:
            opt.mindec = -68
        if opt.maxra is None:
            opt.maxra = 360
        if opt.minra is None:
            opt.minra = 0

    elif opt.kind in ['mzls+bass-dr4', 'mzls+bass-dr4-model', 'mzls+bass-dr4-resid']:
        if opt.maxdec is None:
            opt.maxdec = 90
        if opt.mindec is None:
            opt.mindec = 30
        if opt.maxra is None:
            opt.maxra = 54
        if opt.minra is None:
            opt.minra = 301
    elif opt.kind in ['mzls+bass-dr6', 'mzls+bass-dr6-model', 'mzls+bass-dr6-resid']:
        if opt.maxdec is None:
            opt.maxdec = 90
        if opt.mindec is None:
            opt.mindec = -20
        if opt.maxra is None:
            opt.maxra = 360
        if opt.minra is None:
            opt.minra = 0

    # elif opt.kind in ['dr8', 'dr8-model', 'dr8-resid']:
    #     if opt.maxdec is None:
    #         opt.maxdec = 90
    #     if opt.mindec is None:
    #         opt.mindec = -5
    #     if opt.maxra is None:
    #         opt.maxra = 360
    #     if opt.minra is None:
    #         opt.minra = 0
    
    elif opt.kind in ['dr8-north', 'dr8-north-model', 'dr8-north-resid']:
        if opt.maxdec is None:
            opt.maxdec = 90
        if opt.mindec is None:
            opt.mindec = -5
        if opt.maxra is None:
            opt.maxra = 360
        if opt.minra is None:
            opt.minra = 0

    elif opt.kind in ['dr8-south', 'dr8-south-model', 'dr8-south-resid']:
        if opt.maxdec is None:
            opt.maxdec = 40
        if opt.mindec is None:
            opt.mindec = -70
        if opt.maxra is None:
            opt.maxra = 360
        if opt.minra is None:
            opt.minra = 0

    elif opt.kind in ['decaps2', 'decaps2-model', 'decaps2-resid']:
        if opt.maxdec is None:
            opt.maxdec = -20
        if opt.mindec is None:
            opt.mindec = -70
        if opt.maxra is None:
            opt.maxra = 280
        if opt.minra is None:
            opt.minra = 90
    else:
        if opt.maxdec is None:
            opt.maxdec = 40
        if opt.mindec is None:
            opt.mindec = -25
        if opt.maxra is None:
            opt.maxra = 360
        if opt.minra is None:
            opt.minra = 0

    if opt.bands is None:
        opt.bands = 'grz'

    if opt.top:
        top_levels(mp, opt)
        sys.exit(0)

    if opt.bricks:
        from map.views import get_layer
        layer = get_layer(opt.kind)
        for scale in range(1,8):
            B = layer.get_bricks_for_scale(scale)
        sys.exit(0)

    if opt.scale:

        if opt.kind == 'ps1':
            from map.views import get_layer

            fns = glob('data/ps1/skycells/*/ps1-*.fits')
            fns.sort()
            #ps1-1561-021-r.fits
            if len(opt.zoom) == 0:
                opt.zoom = [1,2,3,4,5,6,7]
            print(len(fns), 'PS1 image files')
            layer = get_layer(opt.kind)
            B = layer.get_bricks()
            for i,brick in enumerate(B):
                for band in opt.bands:
                    fn0 = layer.get_filename(brick, band, 0)
                    if not os.path.exists(fn0):
                        continue
                    for scale in opt.zoom:
                        fn = layer.get_filename(brick, band, scale)
                        layer.create_scaled_image(brick, band, scale, fn)
            sys.exit(0)


        # Rebricked
        if opt.kind in ['decals-dr5', 'decals-dr5-model', 'decals-dr7', 'decals-dr7-model',
                        'eboss',
                        'mzls+bass-dr6', 'mzls+bass-dr6-model',
                        'unwise-neo3', 'unwise-neo4', 'unwise-cat-model',
                        'galex', 'wssa', 'des-dr1', 'hsc', 'hsc2',
                        'dr8-north', 'dr8-north-model', 'dr8-north-resid',
                        'dr8-south', 'dr8-south-model', 'dr8-south-resid',
                        'dr9c',
                    ] or opt.kind.startswith('dr8-test'): # or True:
            from map.views import get_layer

            layer = get_layer(opt.kind)

            if opt.queue:
                if len(opt.zoom) == 0:
                    opt.zoom = [1,2,3,4,5,6,7]
                #step = 0.1
                #ras = np.arange(opt.minra, opt.maxra+step, step)
                step = 3.
                #ras = np.arange(opt.minra, opt.maxra+step, step)
                decs = np.arange(opt.mindec, opt.maxdec+step, step)
                for zoom in opt.zoom:
                    for declo,dechi in zip(decs, np.clip(decs[1:], opt.mindec, opt.maxdec)):
                        rstep = step / np.maximum(0.05, np.cos(np.deg2rad((declo+dechi)/2.)))
                        ras = np.arange(opt.minra, opt.maxra+rstep, rstep)
                        for ralo,rahi in zip(ras, np.clip(ras[1:], opt.minra, opt.maxra)):
                            cmd = ('python render-tiles.py --kind %s --scale --minra %f --maxra %f --mindec %f --maxdec %f -z %i' %
                                   (opt.kind, ralo, rahi, declo, dechi, zoom))
                            print(cmd)
                sys.exit(0)


            if len(opt.zoom) == 0:
                opt.zoom = [1]

            for scale in opt.zoom:
                B = layer.get_bricks_for_scale(scale)
                print(len(B), 'bricks for scale', scale)
                if opt.touching:
                    B.cut((B.dec2 >= opt.mindec) * (B.dec1 <= opt.maxdec))
                    print(len(B), 'touching Dec range')
                    B.cut((B.ra2 >= opt.minra) * (B.ra1 <= opt.maxra))
                    print(len(B), 'touching RA range')
                else:
                    B.cut((B.dec >= opt.mindec) * (B.dec <= opt.maxdec))
                    print(len(B), 'in Dec range')
                    B.cut((B.ra  >= opt.minra)  * (B.ra  <= opt.maxra))
                    print(len(B), 'in RA range')

                bands = opt.bands

                has = {}
                for band in bands:
                    if 'has_%s' % band in B.get_columns():
                        has[band] = B.get('has_%s' % band)
                    else:
                        # assume yes
                        has[band] = np.ones(len(B), bool)

                # Run one scale at a time
                args = []
                for ibrick,brick in enumerate(B):
                    for band in bands:
                        if has[band][ibrick]:
                            args.append((layer, brick, band, scale, opt.ignore))
                print(len(args), 'bricks for scale', scale)
                mp.map(_layer_get_filename, args)

            sys.exit(0)
                
        
        if (opt.kind in ['decals-dr3', 'decals-dr3-model',
                         'mzls+bass-dr4', 'mzls+bass-dr4-model',
                         'decaps2', 'decaps2-model', 'eboss', 'ps1']
            or 'dr8b' in opt.kind
            or 'dr8c' in opt.kind
            or 'dr8i' in opt.kind):

            from map.views import get_survey, get_layer

            surveyname = opt.kind
            # *-model -> *
            # for prefix in ['decals-dr3', 'mzls+bass-dr4', 'decaps2', 'decals-dr5']:
            #     if prefix in surveyname:
            #         surveyname = prefix

            for suffix in ['-model', '-resid']:
                if surveyname.endswith(suffix):
                    surveyname = surveyname[:-len(suffix)]

            survey = get_survey(surveyname)

            print('Survey:', survey)
            print('  cache_dir:', survey.cache_dir)

            B = survey.get_bricks()
            print(len(B), 'bricks')
            B.cut((B.dec >= opt.mindec) * (B.dec < opt.maxdec))
            print(len(B), 'in Dec range')
            B.cut((B.ra  >= opt.minra)  * (B.ra  < opt.maxra))
            print(len(B), 'in RA range')

            # find all image files
            filetype = 'image'
            model = False
            if '-model' in opt.kind:
                model = True
                filetype = 'model'

            bands = opt.bands

            layer = get_layer(opt.kind)

            has = {}
            for band in bands:
                if 'has_%s' % band in B.get_columns():
                    has[band] = B.get('has_%s' % band)
                else:
                    # assume yes
                    has[band] = np.ones(len(B), bool)

            for scale in opt.zoom:
                args = []
                for ibrick,brick in enumerate(B):
                    for band in bands:
                        if not has[band][ibrick]:
                            print('Brick', brick.brickname, 'does not have', band)
                            continue
                        args.append((layer, brick, band, scale, opt.ignore))
                mp.map(_layer_get_filename, args)
                
            sys.exit(0)

        elif opt.kind == 'sdss2':
            layer = get_layer(opt.kind)
            bands = 'gri'
            scales = opt.zoom
            if len(scales) == 0:
                scales = list(range(1,8))
            for scale in scales:
                #maxscale = 7
                bricks = layer.get_bricks_for_scale(scale)
                print('Got', len(bricks), 'bricks for scale', scale)
                bricks.cut((bricks.dec > opt.mindec) * (bricks.dec <= opt.maxdec) *
                           (bricks.ra  > opt.minra ) * (bricks.ra  <= opt.maxra))
                print('Cut to', len(bricks), 'bricks within RA,Dec box')

                for ibrick,brick in enumerate(bricks):
                    for band in bands:
                        print('Scaling brick', ibrick, 'of', len(bricks), 'scale', scale, 'brick', brick.brickname, 'band', band)
                        fn = layer.get_filename(brick, band, scale)
            sys.exit(0)

        if opt.kind in ['unwise-w1w2', 'unwise-neo2']:
            # scaledir = opt.kind
            # basedir = settings.DATA_DIR
            # dirnm = os.path.join(basedir, 'scaled', scaledir)
            # B = fits_table(os.path.join(basedir, 'unwise-bricks.fits'))
            layer = get_layer(opt.kind)
            B = layer.get_bricks()
            print(len(B), 'unWISE tiles')
            for b in B:
                for band in ['1','2']:
                    for scale in [1,2,3,4,5,6,7]:
                        print('Get brick', b.brickname, 'band', band, 'scale', scale)
                        layer.get_filename(b, band, scale)

        else:
            assert(False)


    if opt.bricks_exist:
        from map.views import get_survey

        surveyname = opt.kind
        filetype = 'image'

        survey = get_survey(surveyname)

        B = survey.get_bricks()
        print(len(B), 'bricks')
        B.cut((B.dec >= opt.mindec) * (B.dec < opt.maxdec))
        print(len(B), 'in Dec range')
        B.cut((B.ra  >= opt.minra)  * (B.ra  < opt.maxra))
        print(len(B), 'in RA range')

        # find all image files
        bands = opt.bands

        has_band = {}
        for b in bands:
            B.set('has_%s' % b, np.zeros(len(B), bool))
            has_band[b] = B.get('has_%s' % b)
        exists = np.zeros(len(B), bool)

        for i,brick in enumerate(B.brickname):
            found = False
            for band in bands:
                fn = survey.find_file(filetype, brick=brick, band=band)
                ex = os.path.exists(fn)
                print('Brick', brick, 'band', band, 'exists?', ex)
                has_band[band][i] = ex
                if ex:
                    found = True
            exists[i] = found

        B.cut(exists)
        B.writeto('bricks-exist-%s.fits' % opt.kind)
        sys.exit(0)

    from map.views import get_survey
    surveyname = opt.kind
    if surveyname.endswith('-model'):
        surveyname = surveyname.replace('-model','')
    if surveyname.endswith('-resid'):
        surveyname = surveyname.replace('-resid','')
    survey = get_survey(surveyname)

    if len(opt.zoom) == 0:
        opt.zoom = [13]
    
    if opt.near:
        if opt.kind == 'sdss':
            B = fits_table(os.path.join(settings.DATA_DIR, 'bricks-sdssco.fits'))
        else:
            B = survey.get_bricks()
        print(len(B), 'bricks')

    #if opt.scale:
    #    opt.near_ccds = True

    if opt.near_ccds:
        if opt.kind == 'sdss':
            C = fits_table(os.path.join(settings.DATA_DIR, 'sdss', 'window_flist.fits'),
                           columns=['rerun','ra','dec', 'run', 'camcol', 'field', 'score'])
            C.cut(C.rerun == '301')
            C.cut(C.score >= 0.6)
            #C.delete_column('rerun')
            # SDSS field size
            radius = 1.01 * np.hypot(10., 14.)/2. / 60.
            ccdsize = radius
            print(len(C), 'SDSS fields')

        else:
            C = survey.get_ccds()
            print(len(C), 'CCDs')
            ccdsize = 0.2

    if opt.x is not None:
        opt.x0 = opt.x
        opt.x1 = opt.x + 1
    if opt.y is not None:
        opt.y0 = opt.y
        opt.y1 = opt.y + 1

    if opt.coadd and opt.kind == 'galex':
        layer = GalexLayer('galex')
        
        # base-level (coadd) bricks
        B = layer.get_bricks()
        print(len(B), 'bricks')
        B.cut((B.dec >= opt.mindec) * (B.dec < opt.maxdec))
        print(len(B), 'in Dec range')
        B.cut((B.ra  >= opt.minra)  * (B.ra  < opt.maxra))
        print(len(B), 'in RA range')

        pat = layer.get_scaled_pattern()
        tempfiles = []
        for b in B:
            for band in ['n','f']:
                fn = pat % dict(scale=0, band=band, brickname=b.brickname)
                layer.create_coadd_image(b, band, 0, fn, tempfiles=tempfiles)
            for fn in tempfiles:
                os.unlink(fn)
        sys.exit(0)

    if opt.coadd and opt.kind == 'sdss':
        from legacypipe.survey import wcs_for_brick
        from map.views import trymakedirs

        #B = survey.get_bricks()
        B = fits_table(os.path.join(settings.DATA_DIR, 'sdss2', 'bricks-sdssco.fits'))
        print(len(B), 'bricks')
        B.cut((B.dec >= opt.mindec) * (B.dec < opt.maxdec))
        print(len(B), 'in Dec range')
        B.cut((B.ra  >= opt.minra)  * (B.ra  < opt.maxra))
        print(len(B), 'in RA range')

        if opt.queue:
            # ~ square-degree tiles
            # RA slices
            rr = np.arange(opt.minra , opt.maxra +1)
            dd = np.arange(opt.mindec, opt.maxdec+1)
            for rlo,rhi in zip(rr, rr[1:]):
                for dlo,dhi in zip(dd, dd[1:]):
                    print('time python render-tiles.py --kind sdss --coadd --minra %f --maxra %f --mindec %f --maxdec %f' % (rlo, rhi, dlo, dhi))
            sys.exit(0)

        if opt.grass:
            basedir = settings.DATA_DIR
            codir = os.path.join(basedir, 'coadd', 'sdssco')
            rr,dd = [],[]
            exist = []
            for i,b in enumerate(B):
                print('Brick', b.brickname,)
                fn = os.path.join(codir, b.brickname[:3], 'sdssco-%s-%s.fits' % (b.brickname, 'r'))
                print('-->', fn,)
                if not os.path.exists(fn):
                    print()
                    continue
                print('found')
                rr.append(b.ra)
                dd.append(b.dec)
                exist.append(i)

            exist = np.array(exist)
            B.cut(exist)
            B.writeto('bricks-sdssco-exist.fits')

            import pylab as plt
            plt.clf()
            plt.plot(rr, dd, 'k.')
            plt.title('SDSS coadd tiles')
            plt.savefig('sdss.png')
            sys.exit(0)

        basedir = settings.DATA_DIR
        codir = os.path.join(basedir, 'coadd', 'sdssco')
        for b in B:
            print('Brick', b.brickname)
            wcs = wcs_for_brick(b, W=2400, H=2400, pixscale=0.396)
            #bands = 'gri'
            bands = 'z'

            dirnm = os.path.join(codir, b.brickname[:3])
            fns = [os.path.join(dirnm, 'sdssco-%s-%s.fits' % (b.brickname, band))
                   for band in bands]

            hdr = fitsio.FITSHDR()
            hdr['SURVEY'] = 'SDSS'
            wcs.add_to_header(hdr)

            if all([os.path.exists(fn) for fn in fns]):
                print('Already exist')
                continue

            from map.oldviews import map_sdss

            ims = map_sdss(req, 1, 0, 0, 0, get_images=True, wcs=wcs, ignoreCached=True,
                           forcescale=0, bands=bands)
            if ims is None:
                print('No overlap')
                continue
            trymakedirs(os.path.join(dirnm, 'xxx'))
            for fn,band,im in zip(fns,bands, ims):
                fitsio.write(fn, im, header=hdr, clobber=True)
                print('Wrote', fn)

            # Also write scaled versions
            # dirnm = os.path.join(basedir, 'scaled', 'sdssco')
            # scalepat = os.path.join(dirnm, '%(scale)i%(band)s', '%(brickname).3s', 'sdssco-%(brickname)s-%(band)s.fits')
            # for im,band in zip(ims,bands):
            #     scalekwargs = dict(band=band, brick=b.brickid, brickname=b.brickname)
            #     imwcs = wcs
            #     for scale in range(1, 7):
            #         print('Writing scale level', scale)
            #         im,imwcs,sfn = get_scaled(scalepat, scalekwargs, scale, None,
            #                                   wcs=imwcs, img=im, return_data=True)
        sys.exit(0)


    for zoom in opt.zoom:
        N = 2**zoom
        if opt.y1 is None:
            y1 = N
        else:
            y1 = opt.y1

        if opt.x0 is None:
            opt.x0 = 0
        x1 = opt.x1
        if x1 is None:
            x1 = N

        if opt.split:
            decsplit = 32.
            y = 2.**zoom/(2.*np.pi) * (np.pi - np.log(np.tan(np.pi/4. + np.deg2rad(decsplit)/2.)))
            y = int(y)
            opt.y0 = y
            y1 = y+1

        # Find grid of Ra,Dec tile centers and select the ones near DECaLS bricks.
        rr,dd = [],[]
        yy = np.arange(opt.y0, y1)
        xx = np.arange(opt.x0, x1)

        if opt.grass:
            import pylab as plt
            tileexists = np.zeros((len(yy),len(xx)), bool)

            

            basedir = settings.DATA_DIR
            ver = tileversions[opt.kind][-1]
            tiledir = os.path.join(basedir, 'tiles', opt.kind, '%i'%ver, '%i'%zoom)
            for dirpath,dirnames,filenames in os.walk(tiledir):
                # change walk order
                dirnames.sort()
                if len(filenames) == 0:
                    continue
                print('Dirpath', dirpath)
                #print 'Dirnames', dirnames
                #print 'Filenames', filenames

                # check for symlinks
                if False:
                    fns = []
                    for fn in filenames:
                        fullfn = os.path.join(tiledir, dirpath, fn)
                        if os.path.isfile(fullfn) and not os.path.islink(fullfn):
                            fns.append(fn)
                    print(len(fns), 'of', len(filenames), 'are files (not symlinks)')
                    filenames = fns

                x = os.path.basename(dirpath)
                x = int(x)
                #print 'x', x

                yy = [int(fn.replace('.jpg','')) for fn in filenames]
                #print 'yy', yy
                print(len(yy), 'tiles')
                for y in yy:
                    tileexists[y - opt.y0, x - opt.x0] = True
            plt.clf()
            plt.imshow(tileexists, interpolation='nearest', origin='upper',
                       vmin=0, vmax=1, cmap='gray')
            fn = 'exist-%s-z%02i' % (opt.kind, zoom)
            plt.savefig(fn+'.png')
            fitsio.write(fn+'.fits', tileexists, clobber=True)
            print('Wrote', fn+'.png and', fn+'.fits')

            continue

        if not opt.all:
            for y in yy:
                wcs,W,H,zoomscale,zoom,x,y = get_tile_wcs(zoom, 0, y)
                r,d = wcs.get_center()
                dd.append(d)
            for x in xx:
                wcs,W,H,zoomscale,zoom,x,y = get_tile_wcs(zoom, x, 0)
                r,d = wcs.get_center()
                rr.append(r)
            dd = np.array(dd)
            rr = np.array(rr)
            if len(dd) > 1:
                tilesize = max(np.abs(np.diff(dd)))
                print('Tile size:', tilesize)
            else:
                if opt.near_ccds or opt.near:
                    try:
                        wcs,W,H,zoomscale,zoom,x,y = get_tile_wcs(zoom, 0, opt.y0+1)
                        r2,d2 = wcs.get_center()
                    except:
                        wcs,W,H,zoomscale,zoom,x,y = get_tile_wcs(zoom, 0, opt.y0-1)
                        r2,d2 = wcs.get_center()
                    tilesize = np.abs(dd[0] - d2)
                    print('Tile size:', tilesize)
                else:
                    tilesize = 180.
            I = np.flatnonzero((dd >= opt.mindec) * (dd <= opt.maxdec))
            print('Keeping', len(I), 'Dec points between', opt.mindec, 'and', opt.maxdec)
            dd = dd[I]
            yy = yy[I]

            if opt.near_ccds:
                margin = tilesize + ccdsize
                I = np.flatnonzero((dd > C.dec.min()-margin) * (dd < C.dec.max()+margin))
                if len(I) == 0:
                    print('No Dec points within range of CCDs')
                    continue
                dd = dd[I]
                yy = yy[I]
                print('Keeping', len(I), 'Dec points within range of CCDs: Dec',
                      dd.min(), dd.max())

            I = np.flatnonzero((rr >= opt.minra) * (rr <= opt.maxra))
            print('Keeping', len(I), 'RA points between', opt.minra, 'and', opt.maxra)
            rr = rr[I]
            xx = xx[I]
            
            print(len(rr), 'RA points x', len(dd), 'Dec points')
            print('x tile range:', xx.min(), xx.max(), 'y tile range:', yy.min(), yy.max())

        for iy,y in enumerate(yy):
            print()
            print('Y row', y)

            if opt.queue:

                if 'decaps2' in opt.kind:
                    layer = get_layer(opt.kind)

                    if zoom >= layer.nativescale:
                        oldscale = 0
                    else:
                        oldscale = (layer.nativescale - zoom)
                        oldscale = np.clip(oldscale, layer.minscale, layer.maxscale)

                    x = 0
                    wcs, W, H, zoomscale, z,xi,yi = get_tile_wcs(zoom, x, y)
                    newscale = layer.get_scale(zoom, 0, y, wcs)

                    if oldscale == newscale:
                        print('Oldscale = newscale = ', oldscale)
                        continue
                    
                
                cmd = 'python -u render-tiles.py --zoom %i --y0 %i --y1 %i --kind %s --mindec %f --maxdec %f' % (zoom, y, y+1, opt.kind, opt.mindec, opt.maxdec)
                cmd += ' --threads 32'
                if opt.near_ccds:
                    cmd += ' --near-ccds'
                if opt.all:
                    cmd += ' --all'
                if opt.ignore:
                    cmd += ' --ignore'
                print(cmd)
                continue

            if opt.near:
                d = dd[iy]
                I,J,dist = match_radec(rr, d+np.zeros_like(rr), B.ra, B.dec, 0.25 + tilesize, nearest=True)
                if len(I) == 0:
                    print('No matches to bricks')
                    continue
                keep = np.zeros(len(rr), bool)
                keep[I] = True
                print('Keeping', sum(keep), 'tiles in row', y, 'Dec', d)
                x = xx[keep]
            elif opt.near_ccds:
                d = dd[iy]
                print('RA range of tiles:', rr.min(), rr.max())
                print('Dec of tile row:', d)
                I,J,dist = match_radec(rr, d+np.zeros_like(rr), C.ra, C.dec, ccdsize + tilesize, nearest=True)
                if len(I) == 0:
                    print('No matches to CCDs')
                    continue
                keep = np.zeros(len(rr), bool)
                keep[I] = True
                print('Keeping', sum(keep), 'tiles in row', y, 'Dec', d)
                x = xx[keep]
            else:
                x = xx

            # if opt.grass:
            #     for xi in x:
            #         basedir = settings.DATA_DIR
            #         ver = tileversions[opt.kind][-1]
            #         tilefn = os.path.join(basedir, 'tiles', opt.kind,
            #                               '%i/%i/%i/%i.jpg' % (ver, zoom, xi, y))
            #         print 'Checking for', tilefn
            #         if os.path.exists(tilefn):
            #             print 'EXISTS'
            #             tileexists[yi-opt.y0, xi-opt.x0]
            #     continue

            args = []
            for xi in x:
                args.append((opt.kind,zoom,xi,y, opt.ignore, False))
                #args.append((opt.kind,zoom,xi,y, opt.ignore, True))
            print('Rendering', len(args), 'tiles in row y =', y)
            mp.map(_bounce_one_tile, args, chunksize=min(100, max(1, int(len(args)/opt.threads))))
            #mp.map(_one_tile, args, chunksize=min(100, max(1, int(len(args)/opt.threads))))
            print('Rendered', len(args), 'tiles')

        # if opt.grass:
        #     plt.clf()
        #     plt.plot(tileexists, interpolation='nearest', origin='lower',
        #              vmin=0, vmax=1, cmap='gray')
        #     plt.savefig('%s-z%02i-exists.png' % (opt.kind, zoom))

if __name__ == '__main__':
    main()
