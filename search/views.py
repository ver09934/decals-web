from django.shortcuts import render, redirect
from squrl import unsqurl, squrlup
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.db import connections

def api_search(request, query):
    import numpy as np
    from astropy.io import fits
    from astropy.io.fits import Column

    result = unsqurl(query)
    if result['returncode'] != '200':
        #return error
        return HttpResponse(result['error'])


    print('UNSqurl:', result)

    #run the query
    cursor = connections['cosmo'].cursor()
    cursor.execute(result['sql'])
    rows = cursor.fetchall()
    #return FITS file
    priheader = fits.Header()
    priheader['COMMENT'] = "This file was generated by the Cosmo web portal."
    prihdu = fits.PrimaryHDU(header=priheader)
    # this works if the fields all map directly with no arrays
    # for i in range (0, nrows):
    #     for j in range (0, len(dtypes)):
    #         data[i][dtypes[j][0]] = rows[i][j]
    nrows = len(rows)
    if result['table'] == "DEFAULT":
        # try building from columns
        data = {'cand_id':[],'brickid':[],'objid':[],'type':[],'ra':[],'ra_ivar':[],'dec':[],'dec_ivar':[],'bx':[],'by':[],'bx0':[],'by0':[],'ebv':[],'dchisq':[],
            'fracDev':[],'fracDev_ivar':[],'shapeExp_r':[],'shapeExp_r_ivar':[],'shapeExp_e1':[],'shapeExp_e1_ivar':[],'shapeExp_e2':[],'shapeExp_e2_ivar':[],'shapeDev_r':[], 
            'shapeDev_r_ivar':[],'shapeDev_e1':[],'shapeDev_e1_ivar':[],'shapeDev_e2':[],'shapeDev_e2_ivar':[],'decam_flux':[],'decam_flux_ivar':[],'decam_fracflux':[],
            'decam_fracmasked':[],'decam_fracin':[],'decam_rchi2':[],'decam_nobs':[],'decam_anymask':[],'decam_allmask':[],'decam_mw_transmission':[],'wise_flux':[],
            'wise_flux_ivar':[],'wise_fracflux':[],'wise_rchi2':[],'wise_nobs':[],'wise_mw_transmission':[],'decam_apflux':[],'decam_apflux_resid':[],'decam_apflux_ivar':[],
            }
        for i in range(0,nrows):
            data['cand_id'].append(rows[i][0])
            data['brickid'].append(rows[i][3])
            data['objid'].append(rows[i][4])
            data['type'].append(rows[i][5])
            data['ra'].append(rows[i][6])
            data['ra_ivar'].append(rows[i][7])
            data['dec'].append(rows[i][8])
            data['dec_ivar'].append(rows[i][9])
            data['bx'].append(rows[i][10])
            data['by'].append(rows[i][11])
            data['bx0'].append(rows[i][12])
            data['by0'].append(rows[i][13])
            data['ebv'].append(rows[i][14])
            data['dchisq'].append([rows[i][15],rows[i][16],rows[i][17],rows[i][18]])
            data['fracDev'].append(rows[i][19])
            data['fracDev_ivar'].append(rows[i][20])
            data['shapeExp_r'].append(rows[i][21])
            data['shapeExp_r_ivar'].append(rows[i][22])
            data['shapeExp_e1'].append(rows[i][23])
            data['shapeExp_e1_ivar'].append(rows[i][24])
            data['shapeExp_e2'].append(rows[i][25])
            data['shapeExp_e2_ivar'].append(rows[i][26])
            data['shapeDev_r'].append(rows[i][27])
            data['shapeDev_r_ivar'].append(rows[i][28])
            data['shapeDev_e1'].append(rows[i][29])
            data['shapeDev_e1_ivar'].append(rows[i][30])
            data['shapeDev_e2'].append(rows[i][31])
            data['shapeDev_e2_ivar'].append(rows[i][32])
            data['decam_flux'].append([rows[i][33],rows[i][34],rows[i][35],rows[i][36],rows[i][37],rows[i][38]])
            data['decam_flux_ivar'].append([rows[i][39],rows[i][40],rows[i][41],rows[i][42],rows[i][43],rows[i][44]])
            data['decam_fracflux'].append([rows[i][45],rows[i][46],rows[i][47],rows[i][48],rows[i][49],rows[i][50]])
            data['decam_fracmasked'].append([rows[i][51],rows[i][52],rows[i][53],rows[i][54],rows[i][55],rows[i][56]])
            data['decam_fracin'].append([rows[i][57],rows[i][58],rows[i][59],rows[i][60],rows[i][61],rows[i][62]])
            data['decam_rchi2'].append([rows[i][63],rows[i][64],rows[i][65],rows[i][66],rows[i][67],rows[i][68]])
            data['decam_nobs'].append([rows[i][69],rows[i][70],rows[i][71],rows[i][72],rows[i][73],rows[i][74]])
            data['decam_anymask'].append([rows[i][75],rows[i][76],rows[i][77],rows[i][78],rows[i][79],rows[i][80]])
            data['decam_allmask'].append([rows[i][81],rows[i][82],rows[i][83],rows[i][84],rows[i][85],rows[i][86]])
            data['decam_mw_transmission'].append([rows[i][87],rows[i][88],rows[i][89],rows[i][90],rows[i][91],rows[i][92]])
            data['wise_flux'].append([rows[i][93],rows[i][99],rows[i][105],rows[i][111]])
            data['wise_flux_ivar'].append([rows[i][94],rows[i][100],rows[i][106],rows[i][112]])
            data['wise_fracflux'].append([rows[i][95],rows[i][101],rows[i][107],rows[i][113]])
            data['wise_rchi2'].append([rows[i][96],rows[i][102],rows[i][108],rows[i][114]])
            data['wise_nobs'].append([rows[i][97],rows[i][103],rows[i][109],rows[i][115]])
            data['wise_mw_transmission'].append([rows[i][98],rows[i][104],rows[i][110],rows[i][116]])
            data['decam_apflux'].append([rows[i][118],rows[i][119],rows[i][120],rows[i][121],rows[i][122],rows[i][123],rows[i][124],rows[i][125],rows[i][142],rows[i][143],rows[i][144],rows[i][145],rows[i][146],rows[i][147],rows[i][148],rows[i][149],rows[i][166],rows[i][167],rows[i][168],rows[i][169],rows[i][170],rows[i][171],rows[i][172],rows[i][173],rows[i][190],rows[i][191],rows[i][192],rows[i][193],rows[i][194],rows[i][195],rows[i][196],rows[i][197],rows[i][214],rows[i][215],rows[i][216],rows[i][217],rows[i][218],rows[i][219],rows[i][220],rows[i][221],rows[i][238],rows[i][239],rows[i][240],rows[i][241],rows[i][242],rows[i][243],rows[i][244],rows[i][245]])
            data['decam_apflux_resid'].append([rows[i][126],rows[i][127],rows[i][128],rows[i][129],rows[i][130],rows[i][131],rows[i][132],rows[i][133],rows[i][150],rows[i][151],rows[i][152],rows[i][153],rows[i][154],rows[i][155],rows[i][156],rows[i][157],rows[i][174],rows[i][175],rows[i][176],rows[i][177],rows[i][178],rows[i][179],rows[i][180],rows[i][181],rows[i][198],rows[i][199],rows[i][200],rows[i][201],rows[i][202],rows[i][203],rows[i][204],rows[i][205],rows[i][222],rows[i][223],rows[i][224],rows[i][225],rows[i][226],rows[i][227],rows[i][228],rows[i][229],rows[i][246],rows[i][247],rows[i][248],rows[i][249],rows[i][250],rows[i][251],rows[i][252],rows[i][253]])
            data['decam_apflux_ivar'].append([rows[i][134],rows[i][135],rows[i][136],rows[i][137],rows[i][138],rows[i][139],rows[i][140],rows[i][141],rows[i][158],rows[i][159],rows[i][160],rows[i][161],rows[i][162],rows[i][163],rows[i][164],rows[i][165],rows[i][182],rows[i][183],rows[i][184],rows[i][185],rows[i][186],rows[i][187],rows[i][188],rows[i][189],rows[i][206],rows[i][207],rows[i][208],rows[i][209],rows[i][210],rows[i][211],rows[i][212],rows[i][213],rows[i][230],rows[i][231],rows[i][232],rows[i][233],rows[i][234],rows[i][235],rows[i][236],rows[i][237],rows[i][254],rows[i][255],rows[i][256],rows[i][257],rows[i][258],rows[i][259],rows[i][260],rows[i][261]])

        c0 = Column(name='cand_id', format='J', array=data['cand_id'])
        c1 = Column(name='brickid', format='J', array=data['brickid'])
        c2 = Column(name='objid', format='J', array=data['objid'])
        c3 = Column(name='type', format='10A', array=data['type'])
        c4 = Column(name='ra', format='D', array=data['ra'])
        c5 = Column(name='ra_ivar',format='E', array=data['ra_ivar'])
        c6 = Column(name='dec', format='D', array=data['dec'])
        c7 = Column(name='dec_ivar', format='E', array=data['dec_ivar'])
        c8 = Column(name='bx', format='D', array=data['bx'])
        c9 = Column(name='by', format='D', array=data['by'])
        c10 = Column(name='bx0', format='E', array=data['bx0'])
        c11 = Column(name='by0', format='E', array=data['by0'])
        c12 = Column(name='ebv', format='E', array=data['ebv'])
        c13 = Column(name='dchisq', format='4D', array=data['dchisq'])
        c14 = Column(name='fracDev', format='E', array=data['fracDev'])
        c15 = Column(name='fracDev_ivar', format='E', array=data['fracDev_ivar'])
        c16 = Column(name='shapeExp_r', format='E', array=data['shapeExp_r'])
        c17 = Column(name='shapeExp_r_ivar', format='E', array=data['shapeExp_r_ivar'])
        c18 = Column(name='shapeExp_e1', format='E', array=data['shapeExp_e1'])
        c19 = Column(name='shapeExp_e1_ivar', format='E', array=data['shapeExp_e1_ivar'])
        c20 = Column(name='shapeExp_e2', format='E', array=data['shapeExp_e2'])
        c21 = Column(name='shapeExp_e2_ivar', format='E', array=data['shapeExp_e2_ivar'])
        c22 = Column(name='shapeDev_r', format='E', array=data['shapeDev_r'])
        c23 = Column(name='shapeDev_r_ivar', format='E', array=data['shapeDev_r_ivar'])
        c24 = Column(name='shapeDev_e1', format='E', array=data['shapeDev_e1'])
        c25 = Column(name='shapeDev_e1_ivar', format='E', array=data['shapeDev_e1_ivar'])
        c26 = Column(name='shapeDev_e2', format='E', array=data['shapeDev_e2'])
        c27 = Column(name='shapeDev_e2_ivar', format='E', array=data['shapeDev_e2_ivar'])
        c28 = Column(name='decam_flux', format='6E', array=data['decam_flux'])
        c29 = Column(name='decam_flux_ivar', format='6E', array=data['decam_flux_ivar'])
        c30 = Column(name='decam_fracflux', format='6E', array=data['decam_fracflux'])
        c31 = Column(name='decam_fracmasked', format='6E', array=data['decam_fracmasked'])
        c32 = Column(name='decam_fracin', format='6E', array=data['decam_fracin'])
        c33 = Column(name='decam_rchi2', format='6E', array=data['decam_rchi2'])
        c34 = Column(name='decam_nobs', format='6I', array=data['decam_nobs'])
        c35 = Column(name='decam_anymask', format='6I', array=data['decam_anymask'])
        c36 = Column(name='decam_allmask', format='6I', array=data['decam_allmask'])
        c37 = Column(name='decam_mw_transmission', format='6E', array=data['decam_mw_transmission'])
        c38 = Column(name='wise_flux', format='4E', array=data['wise_flux'])
        c39 = Column(name='wise_flux_ivar', format='4E', array=data['wise_flux_ivar'])
        c40 = Column(name='wise_fracflux', format='4E', array=data['wise_fracflux'])
        c41 = Column(name='wise_rchi2', format='4E', array=data['wise_rchi2'])
        c42 = Column(name='wise_nobs', format='4I', array=data['wise_nobs'])
        c43 = Column(name='wise_mw_transmission', format='4E', array=data['wise_mw_transmission'])
        c44 = Column(name='decam_apflux', format='48E', array=data['decam_apflux'])
        c45 = Column(name='decam_apflux_resid', format='48E', array=data['decam_apflux_resid'])
        c46 = Column(name='decam_apflux_ivar', format='48E', array=data['decam_apflux_ivar'])
        hdu = fits.BinTableHDU.from_columns([c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46])


    elif result['table'] == 'CANDIDATE':
        dtypes = [('brickid','i4'),('objid','i4'),
            ('blob','i8'),('type','S10'),('ra','float64'),('ra_ivar','float64'),('dec','float64'),('dec_ivar','float64'),('bx','float64'),
            ('by','float64'),('bx0','float64'),('by0','float64'),('ebv','float64'),('dchisq1','float64'),('dchisq2','float64'),('dchisq3','float64'),('dchisq4','float64'),
            ('fracdev','float64'),('fracdev_ivar','float64'),('shapeexp_r','float64'),('shapeexp_r_ivar','float64'),('shapeexp_e1','float64'),('shapeexp_e1_ivar','float64'),
            ('shapeexp_e2','float64'),('shapeexp_e2_ivar','float64'),('shapedev_r','float64'),('shapedev_r_ivar','float64'),('shapedev_e1','float64'),('shapedev_e1_ivar','float64'),
            ('shapedev_e2','float64'),('shapedev_e2_ivar','float64')]
        data = np.zeros(nrows, dtype=dtypes)
        for i in range(0,nrows):
            data[i]['brickid'] = rows[i][0]
            data[i]['objid'] = rows[i][1]
            data[i]['blob'] = rows[i][2]
            data[i]['type'] = str(rows[i][3])
            data[i]['ra'] = rows[i][4]
            data[i]['ra_ivar'] = rows[i][5]
            data[i]['dec'] = rows[i][6]
            data[i]['dec_ivar'] = rows[i][7]
            data[i]['bx'] = rows[i][8]
            data[i]['by'] = rows[i][9]
            data[i]['bx0'] = rows[i][10]
            data[i]['by0'] = rows[i][11]
            data[i]['ebv'] = rows[i][12]
            data[i]['dchisq1'] = rows[i][13]
            data[i]['dchisq2'] = rows[i][14]
            data[i]['dchisq3'] = rows[i][15]
            data[i]['dchisq4'] = rows[i][16]
            data[i]['fracdev'] = rows[i][17]
            data[i]['fracdev_ivar'] = rows[i][18]
            data[i]['shapeexp_r'] = rows[i][19]
            data[i]['shapeexp_r_ivar'] = rows[i][20]
            data[i]['shapeexp_e1'] = rows[i][21]
            data[i]['shapeexp_e1_ivar'] = rows[i][22]
            data[i]['shapeexp_e2'] = rows[i][23]
            data[i]['shapeexp_e2_ivar'] = rows[i][24]
            data[i]['shapedev_r'] = rows[i][25]
            data[i]['shapedev_r_ivar'] = rows[i][26]
            data[i]['shapedev_e1'] = rows[i][27]
            data[i]['shapedev_e1_ivar'] = rows[i][28]
            data[i]['shapedev_e2'] = rows[i][29]
            data[i]['shapedev_e2_ivar'] = rows[i][30]
        hdu = fits.BinTableHDU(data, header=priheader)
    elif result['table'] == 'DECAM':
        # try building from columns
        data = {'cand_id':[],'decam_flux':[],'decam_flux_ivar':[],'decam_fracflux':[],'decam_fracmasked':[],'decam_fracin':[],'decam_rchi2':[],'decam_nobs':[],'decam_anymask':[],'decam_allmask':[],'decam_ext':[]}
        for i in range(0,nrows):
            data['cand_id'].append(rows[i][0])
            data['decam_flux'].append([rows[i][1],rows[i][11],rows[i][21],rows[i][31],rows[i][41],rows[i][51]])
            data['decam_flux_ivar'].append([rows[i][2],rows[i][12],rows[i][22],rows[i][32],rows[i][42],rows[i][52]])
            data['decam_fracflux'].append([rows[i][3],rows[i][13],rows[i][23],rows[i][33],rows[i][43],rows[i][53]])
            data['decam_fracmasked'].append([rows[i][4],rows[i][14],rows[i][24],rows[i][34],rows[i][44],rows[i][54]])
            data['decam_fracin'].append([rows[i][5],rows[i][15],rows[i][25],rows[i][35],rows[i][45],rows[i][55]])
            data['decam_rchi2'].append([rows[i][6],rows[i][16],rows[i][26],rows[i][36],rows[i][46],rows[i][56]])
            data['decam_nobs'].append([rows[i][7],rows[i][17],rows[i][27],rows[i][37],rows[i][47],rows[i][57]])
            data['decam_anymask'].append([rows[i][8],rows[i][18],rows[i][28],rows[i][38],rows[i][48],rows[i][58]])
            data['decam_allmask'].append([rows[i][9],rows[i][19],rows[i][29],rows[i][39],rows[i][49],rows[i][59]])
            data['decam_ext'].append([rows[i][10],rows[i][20],rows[i][30],rows[i][40],rows[i][50],rows[i][60]])

        c1 = Column(name='cand_id', format='J', array=data['cand_id'])
        c2 = Column(name='decam_flux', format='6D', array=data['decam_flux'])
        c3 = Column(name='decam_flux_ivar', format='6D', array=data['decam_flux_ivar'])
        c4 = Column(name='decam_fracflux', format='6D', array=data['decam_fracflux'])
        c5 = Column(name='decam_fracmasked', format='6D', array=data['decam_fracmasked'])
        c6 = Column(name='decam_fracin', format='6D', array=data['decam_fracin'])
        c7 = Column(name='decam_rchi2', format='6D', array=data['decam_rchi2'])
        c8 = Column(name='decam_nobs', format='6D', array=data['decam_nobs'])
        c9 = Column(name='decam_anymask', format='6D', array=data['decam_anymask'])
        c10 = Column(name='decam_allmask', format='6D', array=data['decam_allmask'])
        c11 = Column(name='decam_ext', format='6D', array=data['decam_ext'])
        hdu = fits.BinTableHDU.from_columns([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11])
        # dtypes = [('cand_id', 'i4'),('decam_flux',np.float64(6,)),
        #     ('decam_flux_ivar',np.float64(6,)),('decam_fracflux',np.float64(6,)),('decam_fracmasked',np.float64(6,)),('decam_fracin',np.float64(6,)),
        #     ('decam_rchi2',np.float64(6,)),('decam_nobs',np.float64(6,)),('decam_anymask',np.float64(6,)),('decam_allmask',np.float64(6,)),('decam_ext',np.float64(6,))]
        # data = np.zeros((nrows,6), dtype=dtypes)

    elif result['table'] == 'WISE':
        dtypes = [()]
        #line_cand = [ tbdata['brickid'][i], tbdata['objid'][i], tbdata['blob'][i], tbdata['type'][i], tbdata['ra'][i], tbdata['ra_ivar'][i], tbdata['dec'][i], tbdata['dec_ivar'][i], tbdata['bx'][i], tbdata['by'][i], tbdata['bx0'][i], tbdata['by0'][i], bool(lb), bool(oob), tbdata['ebv'][i], tbdata['dchisq'][i][0], tbdata['dchisq'][i][1], tbdata['dchisq'][i][2], tbdata['dchisq'][i][3], tbdata['fracDev'][i], tbdata['fracDev_ivar'][i], tbdata['shapeExp_r'][i], tbdata['shapeExp_r_ivar'][i], tbdata['shapeExp_e1'][i], tbdata['shapeExp_e1_ivar'][i], tbdata['shapeExp_e2'][i], tbdata['shapeExp_e2_ivar'][i], tbdata['shapeDev_r'][i], tbdata['shapeDev_r_ivar'][i], tbdata['shapeDev_e1'][i], tbdata['shapeDev_e1_ivar'][i], tbdata['shapeDev_e2'][i], tbdata['shapeDev_e2_ivar'][i] ]

        # for later
        # ('decam_flux','f8',(3,4)),('decam_flux_ivar','f8',(3,4)),('decam_apflux','f8',(3,4)),
        # ('decam_apflux_resid','f8',(3,4)),('decam_apflux_ivar','f8',(3,4)),('decam_mw_transmission','f8',(3,4)),
        # ('decam_nobs','f8',(3,4)),('decam_rchi2','f8',(3,4)),('decam_fracflux','f8',(3,4)),('decam_fracmasked','f8',(3,4)),
        # ('decam_fracin','f8',(3,4)),('decam_saturated','f8',(3,4)),('out_of_bounds','f8',(3,4)),('decam_anymask','f8',(3,4)),
        # ('decam_allmask','f8',(3,4))
        
    outfile = 'data.fits'

    fits.writeto(outfile, hdu.data, hdu.header, clobber=True)
    fsock = open(outfile,"rb")
    response = StreamingHttpResponse(fsock, content_type='application/fits')
    response['Content-Disposition'] = 'attachment; filename="' + outfile + '"'
    return response

def search_form(request):
    return render(request, "search.html")

def sql_search(request):
    squrlquery = squrlup(request.POST['where_info'])
    squrlquery = 'default/' + squrlquery
    return redirect(api_search, squrlquery)

def search_result(request):
    return HttpResponse("result here")

