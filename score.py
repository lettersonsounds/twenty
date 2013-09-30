from pippi import dsp
from pippi import tune

def ping(maxlen=44100):
    out = ''

    freqs = [ dsp.rand(20,10000) for i in range(4) ]

    tlen = dsp.randint(10, maxlen)

    tones = [ dsp.tone(length=tlen, freq=freq, amp=0.1, wavetype='random') 
            for freq in freqs ]

    tones = [ dsp.split(tone, 64) for tone in tones ]

    pcurves = [ dsp.breakpoint([ dsp.rand() for t in range(len(tones[i]) / 20) ],
            len(tones[i])) for i in range(len(tones)) ]

    tones = [ [ dsp.pan(t, pcurves[i][ti]) for ti, t in enumerate(tones[i]) ] 
            for i in range(len(tones)) ]

    fcurves = [ dsp.breakpoint([ dsp.rand(0.0, 0.5) + 0.5 for t in range(len(tones[i]) / 20) ],
            len(tones[i])) for i in range(len(tones)) ]

    tones = [ [ dsp.transpose(t, fcurves[i][ti] + 0.1) for ti, t in enumerate(tones[i]) ] 
            for i in range(len(tones)) ]

    out = dsp.mix([ dsp.env(''.join(tone), 'random') for tone in tones ])
    out = dsp.env(out, 'random')
    out = dsp.pad(out, 0, dsp.randint(0, maxlen * 6))

    return out

out = ''.join([ ping(dsp.mstf(200)) for i in range(100)])

dsp.write(out, 'twenty')
