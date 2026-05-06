import time
import requests
from django.core.management.base import BaseCommand
from stories.models import DictionaryWord

WORDS = {
    'A1': ['hello','goodbye','yes','no','please','thank','sorry','help','water','food','house','family','mother','father','sister','brother','friend','school','book','pen','table','chair','door','window','car','bus','cat','dog','bird','fish','tree','flower','red','blue','green','white','black','big','small','happy','sad','good','bad','hot','cold','new','old','fast','slow','eat','drink','sleep','walk','run','read','write','speak','listen','open','close','give','take','buy','come','go','see','know','want','like','love','work','play'],
    'A2': ['angry','afraid','tired','hungry','thirsty','bored','excited','lonely','beautiful','ugly','clean','dirty','easy','difficult','safe','dangerous','kitchen','bedroom','bathroom','garden','street','market','hospital','airport','money','price','ticket','problem','answer','question','story','reason','weather','season','summer','winter','spring','autumn','mountain','river','travel','arrive','leave','return','wait','meet','visit','invite','cook','wash','carry','drop','pick','push','pull','start','stop','finish','continue','change','choose','decide','forget','remember','enjoy','learn','teach','think','believe','understand','explain'],
    'B1': ['achieve','advantage','affect','agree','allow','appear','argue','arrange','attempt','avoid','aware','benefit','careful','cause','challenge','character','communicate','compare','compete','complete','confident','connect','consider','contain','contribute','control','convince','cooperate','create','culture','curious','damage','deal','debate','delay','describe','develop','discover','discuss','doubt','dream','earn','encourage','environment','estimate','evidence','examine','expand','experience','express','fail','familiar','focus','freedom','generate','global','goal','government','grow','guide','habit','handle','health','honest','identify','imagine','improve','include','increase','influence','inform','inspire','involve','issue','journey','justice','knowledge','language'],
    'B2': ['abandon','abstract','acknowledge','adapt','adequate','advocate','allocate','analyze','anticipate','assess','assume','attribute','authority','bias','capacity','circumstance','collaborate','collapse','commit','complex','concept','consequence','consistent','construct','contrast','controversy','criteria','critical','deduce','defend','define','demonstrate','derive','design','determine','distinguish','diverse','dominate','elaborate','eliminate','emerge','emphasize','encounter','enforce','enhance','establish','evaluate','evolve','exclude','explicit','exploit','expose','extensive','facilitate','flexible','fundamental','hypothesis','illustrate','implement','imply','incorporate','indicate','individual','infer','integrate','interpret','investigate','isolate','justify','maintain','manipulate','modify','motivate','negotiate','objective','obtain'],
    'C1': ['abate','aberrant','abstain','accentuate','accommodate','accumulate','adamant','adhere','ambiguous','ameliorate','articulate','assert','astute','augment','autonomous','brevity','candid','catalyst','coherent','commemorate','compelling','concede','conducive','confound','connotation','contentious','contradict','converge','corroborate','culminate','debilitate','decipher','depict','discern','disseminate','eloquent','empirical','encompass','envisage','eradicate','evoke','exemplify','exert','extrapolate','feasible','formulate','foster','illuminate','imminent','impede','inception','inherent','innovative','instigate','integrity','intricate','juxtapose','lucid','meticulous','mitigate','nuance','obsolete','permeate','perpetuate','pragmatic','precedent','profound','proliferate','reconcile','refute','reinforce'],
    'C2': ['abstruse','acrimony','adjudicate','alacrity','ambivalence','anachronistic','antithesis','apocryphal','apposite','arcane','assiduous','atrophy','avarice','bellicose','byzantine','capricious','circumlocution','cognizant','commensurate','compendium','concomitant','consternation','contrition','corollary','culpable','deference','deleterious','denouement','deprecate','desultory','diatribe','dichotomy','diffidence','dilettante','discrepancy','dissonance','ebullience','efficacious','egregious','elusive','embroil','endemic','enigmatic','ephemeral','equivocal','erudite','esoteric','exacerbate','fallacious','fastidious','foreboding','garrulous','iconoclast','idiosyncrasy','impetuous','indelible','inexorable','insidious','intransigent','inveterate','laconic','loquacious','mendacious','nefarious','obfuscate','obstreperous','ostentatious','paradigm','perfidious','perspicacious'],
}

def fetch_definition(word):
    try:
        r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}', timeout=6)
        if r.status_code == 200:
            data = r.json()[0]
            phonetic = data.get('phonetic', '')
            meanings = data.get('meanings', [])
            if meanings:
                m = meanings[0]
                word_type = m.get('partOfSpeech', '')
                defs = m.get('definitions', [])
                if defs:
                    return phonetic, word_type, defs[0].get('definition',''), defs[0].get('example','')
    except Exception:
        pass
    return '', '', '', ''

def fetch_translation(word):
    try:
        r = requests.get(f'https://api.mymemory.translated.net/get?q={word}&langpair=en|tr', timeout=6)
        if r.status_code == 200:
            return r.json()['responseData']['translatedText']
    except Exception:
        pass
    return ''

class Command(BaseCommand):
    help = '500+ kelimeyi API den çekip sözlüğe ekler'

    def handle(self, *args, **options):
        total_added = 0
        total_skipped = 0
        for level, words in WORDS.items():
            self.stdout.write(f'\n--- {level} ({len(words)} kelime) ---')
            for i, word in enumerate(words):
                if DictionaryWord.objects.filter(word__iexact=word).exists():
                    total_skipped += 1
                    continue
                phonetic, word_type, definition_en, example = fetch_definition(word)
                meaning_tr = fetch_translation(word)
                DictionaryWord.objects.create(
                    word=word, level=level, phonetic=phonetic,
                    word_type=word_type, definition_en=definition_en,
                    example_sentence=example, meaning_tr=meaning_tr,
                )
                total_added += 1
                self.stdout.write(f'  [{i+1}/{len(words)}] {word} — {meaning_tr or "çeviri yok"}')
                time.sleep(0.4)
        self.stdout.write(f'\n✅ {total_added} eklendi, {total_skipped} atlandı.')