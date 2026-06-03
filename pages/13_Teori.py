import streamlit as st
from utils import show_sidebar_constants, show_resultat_sidebar, breadcrumb

st.set_page_config(page_title="Teorispørgsmål", page_icon="🧠", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("🧠", "Teorispørgsmål")
st.title("🧠 Teorispørgsmål")
st.markdown("Konceptuelle multiple choice-spørgsmål — samme type som DTU 10060 eksamen.  \nPrøv at svare mentalt, tryk derefter **Vis svar** for forklaring.")
st.divider()

QUESTIONS = [
    # ── Kinematik ──────────────────────────────────────────────────────────────
    {
        "emne": "Kinematik",
        "q": "En bold kastes lodret op og lander på samme sted. Hvad er størrelsen af boldens acceleration i toppunktet (hvor v = 0)?",
        "options": ["A) 0 m/s² — bolden er momentant i hvile", "B) g/2 ≈ 4.91 m/s² nedad", "C) g = 9.82 m/s² nedad", "D) g = 9.82 m/s² opad", "E) Afhænger af starthastighed"],
        "correct": "C",
        "explain": "Accelerationen er g = 9.82 m/s² nedad under hele kastet — inklusiv i toppunktet. Acceleration ≠ 0 bare fordi v = 0. Man kan sagtens have nulhastighed men ikke-nul acceleration.",
    },
    {
        "emne": "Kinematik",
        "q": "To projektiler skydes fra samme punkt med samme starthastighed v₀ ved θ = 30° og θ = 60° (ingen luftmodstand). Hvad gælder for deres vandrette rækkevidde?",
        "options": ["A) 30° har størst rækkevidde", "B) 60° har størst rækkevidde", "C) De har præcis samme rækkevidde", "D) 45° er unik — ingen andre par vinkler giver samme rækkevidde", "E) Afhænger af starthastighed"],
        "correct": "C",
        "explain": "x_max = v₀²·sin(2θ)/g. sin(2·30°) = sin(60°) = sin(120°) = sin(2·60°). Komplementære vinkler (θ + φ = 90°) giver altid samme rækkevidde. 45° giver den maksimale.",
    },
    {
        "emne": "Kinematik",
        "q": "Et objekt bevæger sig med konstant acceleration a. Hvad er grafen for position x(t)?",
        "options": ["A) En ret linje", "B) En eksponentialfunktion", "C) En parabel (2.-grads funktion i t)", "D) En konstant", "E) En sinusfunktion"],
        "correct": "C",
        "explain": "x(t) = x₀ + v₀t + ½at² er en andengradspolynomium i t — en parabel. Hastighed v(t) = v₀ + at er en ret linje. Acceleration a(t) = a er en vandret linje.",
    },
    {
        "emne": "Kinematik",
        "q": "En bil bremser med konstant deceleration og stopper efter strækning s. Hvad er bremseafstanden hvis starthastigheden fordobles (samme deceleration)?",
        "options": ["A) 2s", "B) √2·s", "C) 4s", "D) 8s", "E) s er uændret"],
        "correct": "C",
        "explain": "v² = v₀² + 2as → v = 0 giver s = v₀²/(2a). Fordobles v₀: s' = (2v₀)²/(2a) = 4v₀²/(2a) = 4s. Bremseafstanden firedobles — vigtigt i trafiksikkerhed!",
    },
    {
        "emne": "Kinematik",
        "q": "Ved vandret kast fra en klippe: hvad gælder om den vandrette hastigheds­komponent undervejs (ingen luftmodstand)?",
        "options": ["A) Den aftager lineært pga. tyngdekraft", "B) Den er konstant = v₀ under hele kastet", "C) Den stiger grundet tyngdeaccelerationen", "D) Den er nul — kun lodret bevægelse", "E) Den afhænger af kastets varighed"],
        "correct": "B",
        "explain": "Vandret: ingen kraft → ingen acceleration → vandret hastighed = v₀ = konstant. Lodret: tyngdekraft g nedad → v_y = gt (stigende fra 0). De to retninger er fuldstændig uafhængige.",
    },

    # ── Dynamik ─────────────────────────────────────────────────────────────────
    {
        "emne": "Dynamik",
        "q": "En klods hviler på en vandret flade. En vandret kraft F påvirkes klodsen, men den bevæger sig IKKE. Hvad er størrelsen af friktionskraften?",
        "options": ["A) μs·N (maksimal statisk friktion)", "B) μk·N (kinetisk friktion)", "C) Lig med F (reaktiv kraft)", "D) 0", "E) μs·N − F"],
        "correct": "C",
        "explain": "Statisk friktion er reaktiv — den modvirker præcis den aktuelle belastning op til grænsen μs·N. Kun VED grænsen er f = μs·N. Så længe klodsen er i hvile: f = F.",
    },
    {
        "emne": "Dynamik",
        "q": "Hvad ER centripetalkraften for en masse i cirkulær bevægelse?",
        "options": ["A) En ekstra kraft der virker udad fra centrum (centrifugalkraft)", "B) Altid lig tyngdekraften", "C) Nettoresultanten af kræfter der peger mod centrum", "D) Nul, da hastighed er konstant i størrelse", "E) Friktionskraften alene"],
        "correct": "C",
        "explain": "Centripetalkraft er ikke en selvstændig kraft — det er nettokraften F_c = mv²/r mod centrum. Den kan bestå af snorkraft, normalkraft, tyngde eller kombinationer heraf.",
    },
    {
        "emne": "Dynamik",
        "q": "En person trykker mod en væg med kraft F i 10 sekunder. Væggen giver ikke efter. Hvad er det samlede mekaniske arbejde?",
        "options": ["A) F·10 J", "B) F² J", "C) 0 J", "D) Negativt (friktion absorberer energi)", "E) Afhænger af kraftens retning"],
        "correct": "C",
        "explain": "W = F·s·cosθ. Forflytning s = 0 (væggen bevæger sig ikke) → W = 0, uanset kraft og tid. Muskler udfører biologisk/kemisk arbejde, men MEKANISK arbejde er nul.",
    },
    {
        "emne": "Dynamik",
        "q": "En satellit kredser i stabil cirkulær bane om Jorden. Hvad er gravitationens arbejde på satellitten i ét fuldt omløb?",
        "options": ["A) Positivt — tyngden accelererer satellitten", "B) Negativt — tyngden bremser satellitten", "C) 0 — satellitten bevæger sig konstant vinkelret på gravitationen", "D) Afhænger af baneradius", "E) Nul kun for cirkulær bane"],
        "correct": "C",
        "explain": "I cirkulær bane er gravitationen altid rettet mod centrum, mens hastighed er tangential (vinkelret på F). W = F·s·cos(90°) = 0. Tyngden leverer centripetalkraften men udfører intet arbejde.",
    },
    {
        "emne": "Dynamik",
        "q": "En masse glider ned ad et friktionsfrit skråplan med hældningsvinkel θ. Hvad er accelerationen langs planen?",
        "options": ["A) g", "B) g·cosθ", "C) g·sinθ", "D) g·tanθ", "E) g/(sinθ)"],
        "correct": "C",
        "explain": "Langs planen: F = mg·sinθ. Newton: ma = mg·sinθ → a = g·sinθ. Normalkraft N = mg·cosθ (vinkelret på planen, udfører intet arbejde).",
    },

    # ── Energi ──────────────────────────────────────────────────────────────────
    {
        "emne": "Energi",
        "q": "En bold glider uden friktion ned ad en kurvet bane fra højde h. Hvad bestemmer hastigheden i bunden?",
        "options": ["A) Banens form og hældning", "B) Boldens masse", "C) Kun starthøjden h", "D) Starthøjde og banemateriale", "E) Startfart og højde"],
        "correct": "C",
        "explain": "Energibevarelse: mgh = ½mv² → v = √(2gh). Massen går ud! Banens form spiller ingen rolle uden friktion. Kun h bestemmer v — uanset om banen er ret, kurvet eller spiralet.",
    },
    {
        "emne": "Energi",
        "q": "En fjeder komprimeres til det dobbelte — 2x i stedet for x. Med hvilken faktor øges den lagrede potentielle energi?",
        "options": ["A) 2", "B) √2", "C) 4", "D) 8", "E) Afhænger af fjederkonstanten k"],
        "correct": "C",
        "explain": "E_fjeder = ½kx². Fordobles x: E' = ½k(2x)² = 4·(½kx²). Faktor 4! Kvadratisk sammenhæng. Sækerhedsline og stødabsorbere udnytter dette.",
    },
    {
        "emne": "Energi",
        "q": "Er mekanisk energi (E_k + E_p) altid bevaret?",
        "options": ["A) Ja — det er en fundamental naturlov", "B) Kun ved elastiske kollisioner", "C) Nej — kun bevaret hvis alle kræfter er konservative (ingen friktion, ingen luftmodstand)", "D) Kun i lukkede systemer", "E) Ja, men kun i vakuum"],
        "correct": "C",
        "explain": "Mekanisk energi bevares KUN hvis alle kræfter er konservative (tyngde, fjeder). Friktion, luftmodstand og inelastisk deformation omdanner mekanisk energi til varme. Samlet energi er altid bevaret — men ikke nødvendigvis den mekaniske del.",
    },
    {
        "emne": "Energi",
        "q": "En bold kastes op og kommer ned til samme højde. Hvad er det nettofysiske arbejde udført af tyngdekraften?",
        "options": ["A) Positivt: 2mgh", "B) Negativt: −2mgh", "C) 0 — tyngdekraft er konservativ, lukket sti", "D) mgh", "E) Afhænger af kastets varighed"],
        "correct": "C",
        "explain": "Tyngdekraft er konservativ. Arbejde over en lukket sti = 0. Op: W = −mgh (kraft nedad, bevægelse opad). Ned: W = +mgh. Netto = 0.",
    },

    # ── Elektricitet ────────────────────────────────────────────────────────────
    {
        "emne": "Elektricitet",
        "q": "To modstande R₁ og R₂ er koblet i serie. Hvad gælder for strøm og spænding?",
        "options": ["A) Samme spænding over begge; strøm deles", "B) Samme strøm; spænding fordeles proportonalt med modstand", "C) R_total = R₁·R₂/(R₁+R₂)", "D) R_total < min(R₁, R₂)", "E) Strøm og spænding er ens begge steder"],
        "correct": "B",
        "explain": "Seriekobling: ét strømbane → samme strøm I = U/(R₁+R₂). Spændingsfaldet fordeles: U₁ = IR₁, U₂ = IR₂. R_total = R₁+R₂. (Parallelkobling: R_total = R₁R₂/(R₁+R₂), samme spænding).",
    },
    {
        "emne": "Elektricitet",
        "q": "En kondensator er fuldt opladet i et DC-kredsløb (stationær tilstand). Hvad er strømmen gennem den?",
        "options": ["A) U/R", "B) C·U", "C) 0 — kondensatoren blokerer DC i stationær tilstand", "D) Stiger med tiden", "E) C·dU/dt"],
        "correct": "C",
        "explain": "Fuldt opladet kondensator: ingen yderligere ladningsopbygning → I = 0. Kondensatoren fungerer som åbent kredsløb for DC. Under opladning: I(t) = (U/R)·e^(−t/RC), tidskonstant τ = RC.",
    },
    {
        "emne": "Elektricitet",
        "q": "Lorentzkraft på en ladning q der bevæger sig PARALLELT med magnetfelt B: hvad er kraften?",
        "options": ["A) F = qvB", "B) F = qvB/2", "C) F = 0", "D) F = qB/v", "E) F = q²vB"],
        "correct": "C",
        "explain": "F = qvB·sinθ. Parallelt med B: θ = 0° → sin(0°) = 0 → F = 0. Maksimal kraft når v ⊥ B: F = qvB. Kraften er altid vinkelret på både v og B.",
    },

    # ── Bølger & Optik ──────────────────────────────────────────────────────────
    {
        "emne": "Bølger & Optik",
        "q": "Lysets hastighed i et medium med brydningsindeks n = 1.5 er:",
        "options": ["A) 1.5c ≈ 4.5×10⁸ m/s", "B) c/1.5 ≈ 2.0×10⁸ m/s", "C) c = 3.0×10⁸ m/s (uændret)", "D) c − 1.5 m/s", "E) Afhænger kun af frekvensen"],
        "correct": "B",
        "explain": "n = c/v_medium → v = c/n = 3×10⁸/1.5 = 2×10⁸ m/s. Lyset bremser i mediet. Frekvensen forbliver den samme, men bølgelængden forkortes: λ_medium = λ_vakuum/n.",
    },
    {
        "emne": "Bølger & Optik",
        "q": "Konstruktiv interferens i Young's dobbeltspalte opstår når vejlængdeforskellen ΔL er:",
        "options": ["A) ΔL = λ/2, 3λ/2, 5λ/2, ...", "B) ΔL = 0, λ, 2λ, 3λ, ...", "C) ΔL = λ/4, λ/2, ...", "D) ΔL kan have en vilkårlig værdi", "E) ΔL = nλ kun for n > 0"],
        "correct": "B",
        "explain": "Konstruktiv: ΔL = nλ (n = 0, ±1, ±2, ...) — bølgerne er i fase og summer op. Destruktiv: ΔL = (n + ½)λ — modsat fase, udligner hinanden.",
    },
    {
        "emne": "Bølger & Optik",
        "q": "En lydsender bevæger sig mod en stationær lytter. Hvad hører lytteren sammenlignet med senderens egne frekvens?",
        "options": ["A) Lavere frekvens (rød-skift)", "B) Højere frekvens (blå-skift)", "C) Samme frekvens, men højere lydstyrke", "D) Samme frekvens", "E) Ingen lyd — bølgerne udligner hinanden"],
        "correct": "B",
        "explain": "Doppler: f_obs = f_s·v_lyd/(v_lyd − v_s). Sender nærmer sig → nævner mindskes → f_obs > f_s (højere tone). Ambulance der nærmer sig lyder skarp; fjerner sig lyder dyb.",
    },
    {
        "emne": "Bølger & Optik",
        "q": "I Young's dobbeltspalte: hvad sker med afstanden mellem lyse maksima, hvis bølgelængden λ fordobles (samme d og L)?",
        "options": ["A) Afstanden halveres", "B) Afstanden fordobles", "C) Uændret", "D) Mønsteret forsvinder", "E) Maksima rykker tættere mod centrum"],
        "correct": "B",
        "explain": "y_n = nλL/d. Fordobles λ → y_n fordobles. Større bølgelængde → mere diffraktion → bredere mønster. Rødt lys (stor λ) spreder mere end blåt lys (lille λ).",
    },

    # ── Termodynamik ────────────────────────────────────────────────────────────
    {
        "emne": "Termodynamik",
        "q": "En ideel gas komprimeres isotermt (konstant temperatur). Hvad sker med trykket?",
        "options": ["A) Trykket falder proportionalt", "B) Trykket er uændret", "C) Trykket stiger (Boyles lov: pV = konst)", "D) Trykket stiger kun hvis temperaturen stiger", "E) Afhænger af gastypen"],
        "correct": "C",
        "explain": "Isoterm: T = konst → pV = nRT = konst (Boyles lov). V ↓ → p ↑. Halveres volumen → trykket fordobles. Brug en p-V-graf: isoterm er en hyperbel.",
    },
    {
        "emne": "Termodynamik",
        "q": "I en adiabatisk proces gælder:",
        "options": ["A) Temperaturen er konstant (isoterm)", "B) Trykket er konstant (isobar)", "C) Volumen er konstant (isochor)", "D) Varmeudveksling Q = 0", "E) Intern energi ΔU = 0"],
        "correct": "D",
        "explain": "Adiabatisk: Q = 0. 1. termodynamikslov: ΔU = Q − W → ΔU = −W. Gas afkøles ved adiabatisk ekspansion (udfører arbejde uden varmetilgang). Eks: diesel-motor og atmosfæriske processer.",
    },
    {
        "emne": "Termodynamik",
        "q": "To identiske beholdere med ideel gas ved samme T og p. Den ene er N₂ (M = 28 g/mol), den anden O₂ (M = 32 g/mol). Hvilken indeholder flest molekyler?",
        "options": ["A) N₂ har flest (lettere molekyler, mere plads)", "B) O₂ har flest", "C) Præcis det samme antal (Avogadros lov: pV = nRT)", "D) Afhænger af temperaturen", "E) Kan ikke afgøres"],
        "correct": "C",
        "explain": "Ideel gaslov: n = pV/(RT). Samme p, V og T → samme mol-antal n → samme molekylantal N = n·N_A. (Avogadros lov: ens T, p, V giver ens molantal uanset gasart.) Molmassen spiller ingen rolle!",
    },

    # ── Atomfysik ───────────────────────────────────────────────────────────────
    {
        "emne": "Atomfysik",
        "q": "Hvad er forholdet mellem henfaldskonstant λ og halvvejstid T½?",
        "options": ["A) λ = T½·ln(2)", "B) λ = T½/ln(2)", "C) λ = ln(2)/T½ ≈ 0.693/T½", "D) λ = 1/T½", "E) λ = T½²"],
        "correct": "C",
        "explain": "T½ = ln(2)/λ (fra N = N₀·e^(−λt), sæt N = N₀/2 og løs). Isoler λ: λ = ln(2)/T½. Kortere halvvejstid → større λ → hurtigere henfald.",
    },
    {
        "emne": "Atomfysik",
        "q": "Fotoelektrisk effekt: hvad bestemmer om en elektron frigives fra en metalplade?",
        "options": ["A) Lysets intensitet (antal fotoner)", "B) Lysets frekvens — skal overstige tærskelfrekvens f₀ = W/h", "C) Metallets temperatur", "D) Lysets polarisation", "E) Antallet af elektroner i overfladen"],
        "correct": "B",
        "explain": "Elektroner frigives kun hvis E_foton = hf > W (arbejdsfunktion). Frekvensen bestemmer dette, ikke intensiteten. Selv ekstremt kraftigt lavfrekvent lys frigiver ingen elektroner. Einstein (Nobelpris 1921).",
    },
    {
        "emne": "Atomfysik",
        "q": "En α-partikel består af:",
        "options": ["A) 1 proton og 1 neutron (deuterium)", "B) 2 protoner og 2 neutroner (helium-4-kerne)", "C) 2 elektroner og 2 protoner", "D) En positron", "E) 4 protoner"],
        "correct": "B",
        "explain": "α-partikel = ⁴₂He-kerne: 2 protoner + 2 neutroner. Ladning +2e, masse ≈ 4u. Tungt ioniserende men ringe gennemtrængende (stoppes af papir). Udsendes ved α-henfald fra tunge kerner.",
    },
    {
        "emne": "Atomfysik",
        "q": "De Broglie-bølgelængde: en hurtigere bevægende partikel (samme masse, større kinetisk energi) har:",
        "options": ["A) Større bølgelængde", "B) Mindre bølgelængde", "C) Samme bølgelængde — kun masse bestemmer λ", "D) Bølgelængde = 0 ved høj hastighed", "E) Afhænger af partiklens ladning"],
        "correct": "B",
        "explain": "λ = h/(mv) = h/p. Større v → større impuls p = mv → λ = h/p mindskes. Elektroner i et transmissions-elektronmikroskop accelereres til høj hastighed for at få lille λ og dermed høj opløsning.",
    },

    # ── Usikkerhed ──────────────────────────────────────────────────────────────
    {
        "emne": "Usikkerhed",
        "q": "Hvad er standardmåleusikkerheden (type A) for n gentagne målinger med standardafvigelse s?",
        "options": ["A) u = s", "B) u = s·√n", "C) u = s/√n  (SEM — Standard Error of the Mean)", "D) u = s²/n", "E) u = n/s"],
        "correct": "C",
        "explain": "Type A: u = s/√n. Flere målinger reducerer usikkerheden — men langsomt. 4× så mange målinger halverer usikkerheden. s er spredningen på enkeltmålingerne; u er vores usikkerhed på gennemsnittet.",
    },
    {
        "emne": "Usikkerhed",
        "q": "Fejlpropagation for z = x · y: hvad er den relative usikkerhed Δz/z (RSS-metode)?",
        "options": ["A) Δz/z = Δx·Δy", "B) Δz/z = Δx/x + Δy/y  (worst-case/lineær)", "C) Δz/z = √((Δx/x)² + (Δy/y)²)  (RSS)", "D) Δz = √(Δx² + Δy²)", "E) Δz/z = (Δx/x)·(Δy/y)"],
        "correct": "C",
        "explain": "RSS (Root Sum of Squares) er standard ved DTU 10060 for ukorrelerede bidrag. Worst-case (B) er mere konservativt men overestimerer usikkerheden. For z = x+y gælder derimod Δz = √(Δx²+Δy²).",
    },
    {
        "emne": "Usikkerhed",
        "q": "En lineær regression giver R² = 0.97. Hvad betyder det?",
        "options": ["A) 97% af datapunkterne ligger på linjen", "B) 97% af variansen i y-data forklares af den lineære model", "C) Usikkerheden er 3%", "D) Hældningen a = 0.97", "E) 97% sandsynlighed for at modellen er korrekt"],
        "correct": "B",
        "explain": "R² (determinationskoefficient): andelen af variansen (spredningen) i y forklaret af x via den lineære model. R² = 1: perfekt fit. R² = 0: ingen lineær sammenhæng. R² = 0.97 er et meget godt fit.",
    },
    {
        "emne": "Usikkerhed",
        "q": "Hvad er en type B usikkerhed?",
        "options": ["A) Statistisk usikkerhed fra gentagne målinger (SEM)", "B) Usikkerhed estimeret ud fra andet end statistik — fx instrumentopløsning, kalibrering, fabrikantdata", "C) Usikkerhed der altid er dobbelt så stor som type A", "D) Systematisk fejl der ikke kan korrigeres", "E) Usikkerhed kun relevant for digitale instrumenter"],
        "correct": "B",
        "explain": "Type B: usikkerhed IKKE fra statistisk behandling af gentagne målinger. Fx: voltmeter ±0.5% (fabrikant), lineal aflæsning ±0.5 mm, temperatursensor ±0.1 K. Kombineres med type A via RSS: u_total = √(u_A² + u_B²).",
    },

    # ── Rotation ────────────────────────────────────────────────────────────────
    {
        "emne": "Rotation",
        "q": "En figurdrejer trækker armene ind under rotation (ingen ydre kraftmomenter). Hvad sker der?",
        "options": ["A) Vinkelhastighed ω falder; impulsmoment L bevaret", "B) Vinkelhastighed ω stiger; impulsmoment L bevaret", "C) ω er uændret; inertimoment I bevaret", "D) Rotationsenergi bevares; ω stiger", "E) Begge ω og L stiger"],
        "correct": "B",
        "explain": "L = Iω = konst (ingen ydre kraftmoment). Armene trækkes ind → I falder (masse tættere på aksen) → ω stiger. Rotationsenergi STIGER (muskler udfører arbejde), men L er bevaret.",
    },
    {
        "emne": "Rotation",
        "q": "Hvad er inertimoment-koefficienten c_I for en massiv kugle? (I = c_I · mR²)",
        "options": ["A) c_I = 1 (tynd ring)", "B) c_I = 1/2 (massiv cylinder)", "C) c_I = 2/3 (hul kugle)", "D) c_I = 2/5 (massiv kugle)", "E) c_I = 3/5"],
        "correct": "D",
        "explain": "Massiv kugle: I = (2/5)mR². Husk rækkefølgen (mindst til størst): massiv kugle 2/5 < massiv cylinder 1/2 < hul kugle 2/3 < tynd ring 1. Jo mere masse tæt på aksen, jo lavere c_I.",
    },
    {
        "emne": "Rotation",
        "q": "En massiv kugle og en tynd ring med samme m og R ruller ned ad samme skråning fra samme højde. Hvem ankommer hurtigst i bunden?",
        "options": ["A) Ringen — den har mere rotationsenergi i reserve", "B) Kuglen — lavere c_I, mere energi til translation", "C) De ankommer simultant", "D) Afhænger af skråningens hældning", "E) Afhænger af massen"],
        "correct": "B",
        "explain": "v = √(2gh/(1+c_I)). Kugle: c_I = 2/5 → v = √(2gh/1.4). Ring: c_I = 1 → v = √(2gh/2). Lavere c_I → mere energi til translation → hurtigere. Kuglen vinder altid over ringen.",
    },
    {
        "emne": "Rotation",
        "q": "Steiners sætning I = I_cm + md² bruges til at:",
        "options": ["A) Omregne lineær til vinkelacceleration", "B) Beregne kraftmoment fra inertimoment", "C) Finde inertimoment om en akse parallel med cm-aksen, men forskydt en afstand d", "D) Beregne rulningsenergi", "E) Finde perioden for et simpelt pendul"],
        "correct": "C",
        "explain": "Steiners sætning parallelforskyder aksen fra massemidtpunktet (I_cm) til en parallel akse i afstanden d. I = I_cm + md². Eks: en cylinder der roterer om sin kant har I = ½mR² + mR² = 3/2·mR².",
    },
    {
        "emne": "Rotation",
        "q": "Et kraftmoment τ virker på et legeme med inertimoment I. Hvad er den angulære acceleration α?",
        "options": ["A) α = I·τ", "B) α = τ/I", "C) α = I/τ", "D) α = τ·I²", "E) α = √(τ/I)"],
        "correct": "B",
        "explain": "Newtons 2. lov for rotation: τ = I·α → α = τ/I. Analogt med F = ma → a = F/m. Stort inertimoment → lille vinkelacceleration for samme kraftmoment (svær at sætte i gang).",
    },

    # ── Kollisioner ─────────────────────────────────────────────────────────────
    {
        "emne": "Kollisioner",
        "q": "I en fuldstændig uelastisk kollision gælder:",
        "options": ["A) Kinetisk energi bevaret; impuls ikke bevaret", "B) Impuls bevaret; kinetisk energi IKKE bevaret", "C) Hverken impuls eller kinetisk energi bevaret", "D) Kun kinetisk energi bevaret", "E) Begge bevaret"],
        "correct": "B",
        "explain": "Impuls bevares altid ved kollisioner (Newtons 3. lov, ingen ydre kræfter). Kinetisk energi omdannes til varme/deformation. Fuldstændig uelastisk: objekterne klæber sammen — maksimalt KE-tab.",
    },
    {
        "emne": "Kollisioner",
        "q": "En bold med masse m og hastighed v rammer elastisk head-on en stilstående bold med samme masse m. Hvad sker der?",
        "options": ["A) Begge bevæger sig med v/2 efter stødet", "B) Den første stopper; den anden bevæger sig med v", "C) Begge stopper", "D) Den første bouncer tilbage med −v; den anden forbliver i hvile", "E) Den første bevæger sig med v/3; den anden med 2v/3"],
        "correct": "B",
        "explain": "Elastisk kollision med ens masser: v₁' = (m₁−m₂)v₁/(m₁+m₂) = 0, v₂' = 2m₁v₁/(m₁+m₂) = v₁. Newton's cradle-princippet — fuldstændig overførsel af bevægelse.",
    },
    {
        "emne": "Kollisioner",
        "q": "Massemidtpunktet for et system af to legemer bevæger sig med konstant hastighed når:",
        "options": ["A) Legemerne har samme masse", "B) Der er ingen ydre kræfter på systemet", "C) Kollisionen er elastisk", "D) Legemerne er identiske", "E) Altid — massemidtpunktet bevæger sig altid konstant"],
        "correct": "B",
        "explain": "v_cm = p_total/m_total. Ingen ydre kræfter → impulsbevarelse → p_total = konst → v_cm = konst. Gælder uanset kollisionstype. Indre kræfter (kollisionskræfterne) kan aldrig ændre massemidtpunktets bevægelse.",
    },

    # ── Svingninger ─────────────────────────────────────────────────────────────
    {
        "emne": "Svingninger",
        "q": "En fjedermasse-system har periode T. Hvad sker med perioden hvis massen fordobles (samme fjeder)?",
        "options": ["A) T fordobles", "B) T halveres", "C) T ganges med √2 ≈ 1.41", "D) T er uændret", "E) T afhænger af amplitude"],
        "correct": "C",
        "explain": "T = 2π√(m/k). Fordobles m: T' = 2π√(2m/k) = √2·T ≈ 1.41·T. T er proportional med √m — ikke m. NB: amplituden påvirker IKKE perioden for idealfjeder.",
    },
    {
        "emne": "Svingninger",
        "q": "Et simpelt pendul (T = 2π√(L/g)) og et fjedermasse-system (T = 2π√(m/k)) har begge T = 1 s. Massen fordobles på begge systemer. Hvad sker?",
        "options": ["A) Begge perioder fordobles", "B) Pendulets periode er uændret; fjederens øges med faktor √2", "C) Begge perioder øges med √2", "D) Fjederens er uændret; pendulets øges", "E) Begge perioder er uændrede"],
        "correct": "B",
        "explain": "Pendul: T = 2π√(L/g) — afhænger IKKE af massen! Uændret. Fjedermasse: T = 2π√(m/k) — afhænger af massen. Fordobles m: T_fjeder → √2·T_fjeder.",
    },
    {
        "emne": "Svingninger",
        "q": "Et SHM-system er ved maksimal udslæng (x = A). Hvad gælder?",
        "options": ["A) Hastighed er maksimal; acceleration er nul", "B) Hastighed er nul; acceleration er maksimal (|a| = Aω²)", "C) Begge er nul", "D) Begge er maksimale", "E) Afhænger af systemets energi"],
        "correct": "B",
        "explain": "v(t) = −Aω·sin(ωt+φ). Ved x = ±A: v = 0. a(t) = −Aω²·cos(ωt+φ). Ved x = ±A: |a| = Aω² = maksimal. Fjederkraften F = −kx er størst ved maksimal udslæng.",
    },
    {
        "emne": "Svingninger",
        "q": "Hvad sker med resonansfrekvensen ω_res i et dæmpet svingningssystem sammenlignet med ω₀?",
        "options": ["A) ω_res = ω₀  (uændret)", "B) ω_res > ω₀  (dæmpning hæver resonansen)", "C) ω_res < ω₀  (dæmpning sænker resonansen)", "D) ω_res = 0 ved enhver dæmpning", "E) ω_res = ω₀/2 altid"],
        "correct": "C",
        "explain": "ω_res = √(ω₀² − 2γ²) < ω₀. For svag dæmpning (γ ≪ ω₀) er ω_res ≈ ω₀. Stærk dæmpning: resonanstoppen fladbundes og forskydes mod lavere frekvenser.",
    },

    # ── Relativitetsteori ───────────────────────────────────────────────────────
    {
        "emne": "Relativitetsteori",
        "q": "Hvad er Lorentz-faktoren γ for et objekt i hvile (v = 0)?",
        "options": ["A) γ = 0", "B) γ = ½", "C) γ = 1", "D) γ → ∞", "E) γ = c"],
        "correct": "C",
        "explain": "γ = 1/√(1−v²/c²). Ved v = 0: γ = 1. γ ≥ 1 altid. Relativistiske effekter (tidsudvidelse, længdeforkortning) er proportionale med γ og bliver mærkbare først ved v > 0.1c.",
    },
    {
        "emne": "Relativitetsteori",
        "q": "En observatør ser et ur der bevæger sig forbi med høj hastighed. Hvad observerer den stationære observatør?",
        "options": ["A) Uret går hurtigere (tidskompression)", "B) Uret går langsommere (tidsudvidelse)", "C) Uret går med samme hastighed", "D) Afhænger af urtype", "E) Uret går baglæns"],
        "correct": "B",
        "explain": "Δt = γ·Δt₀ ≥ Δt₀. Det bevægende ur går langsommere set fra den stationære. 'Moving clocks run slow.' GPS-satellitter kompenserer dagligt for ~7 μs tidsforskydning fra specialrelativitet (ur går for langsomt) minus 45 μs fra generelrelativitet (ur går for hurtigt ved højde).",
    },
    {
        "emne": "Relativitetsteori",
        "q": "Hvad er hvileenergien for en partikel med hvile-masse m₀?",
        "options": ["A) E = ½m₀c²", "B) E = m₀c²", "C) E = γm₀c²  (totalenergi)", "D) E = m₀c²/γ", "E) E = 0  (kun bevægende partikler har energi)"],
        "correct": "B",
        "explain": "E₀ = m₀c² er hvileenergien. Totalenergi: E = γm₀c². Kinetisk energi: Ek = (γ−1)m₀c². For v = 0: γ = 1 → E = m₀c². Proton: E₀ ≈ 938 MeV.",
    },

    # ── Dimensionsanalyse ──────────────────────────────────────────────────────
    {
        "emne": "Dimensionsanalyse",
        "q": "Hvilken af følgende størrelser er dimensionsløs?",
        "options": ["A) v²/g  [= L]", "B) v/√(gL)  [= 1]", "C) gL/v  [= LT⁻¹]", "D) v·t  [= L]", "E) F/m  [= LT⁻²]"],
        "correct": "B",
        "explain": "v/√(gL): [LT⁻¹]/√[LT⁻²·L] = [LT⁻¹]/[LT⁻¹] = [1]. Dette er Froude-tallet — bruges i bølge- og skibs­hydrodynamik. De andre giver enheder L, LT⁻¹ osv.",
    },
    {
        "emne": "Dimensionsanalyse",
        "q": "En model har variablerne F [MLT⁻²], m [M], L [L] og t [T]. Hvor mange dimensionsløse Pi-grupper giver Buckinghams teorem?",
        "options": ["A) 0", "B) 1", "C) 2", "D) 3", "E) 4"],
        "correct": "B",
        "explain": "Π = n − k = 4 variable − 3 grunddimensioner (M, L, T) = 1 Pi-gruppe. For eksempel Π = F·t²/(m·L) = [MLT⁻²·T²/(M·L)] = [1] ✓.",
    },
    {
        "emne": "Dimensionsanalyse",
        "q": "Er formlen E = ½mv² dimensionshomogen? (E = energi [ML²T⁻²], m = masse [M], v = hastighed [LT⁻¹])",
        "options": ["A) Nej — [M·L²T⁻²] ≠ [M·LT⁻¹]", "B) Nej — dimensionerne matcher kun halvt", "C) Ja — [M·(LT⁻¹)²] = [ML²T⁻²] ✓", "D) Nej — konstanten ½ ødelægger homogeniteten", "E) Kun hvis man inkluderer c²"],
        "correct": "C",
        "explain": "[½mv²] = [M·(LT⁻¹)²] = [ML²T⁻²] = [energi]. Konstanter (½, 2π, ln2 osv.) er dimensionsløse og påvirker ikke dimensionstjekket. Formlen er korrekt dimensioneret.",
    },
    {
        "emne": "Dimensionsanalyse",
        "q": "I modellen for en penduls periode T = f(m, L, g) — hvad forudsiger dimensionsanalyse?",
        "options": ["A) T = konstant·m/√(Lg)", "B) T = konstant·√(L/g)  (uafhængig af m)", "C) T = konstant·L/g", "D) T = konstant·m·√(L/g)", "E) T = konstant·g/L"],
        "correct": "B",
        "explain": "T [T] fra m [M], L [L], g [LT⁻²]: T ∝ mᵃ·Lᵇ·gᶜ. M: a=0, L: b+c=0, T: −2c=1 → c=−½, b=½. Altså T ∝ √(L/g) — masse indgår slet ikke! Det bekræftes af den eksakte formel T=2π√(L/g).",
    },
    {
        "emne": "Dimensionsanalyse",
        "q": "Hvad er dimensionen af Plancks konstant h, givet at E = h·f (E: energi, f: frekvens)?",
        "options": ["A) [ML²T⁻²]  (energi)", "B) [ML²T⁻¹]  (energi × tid)", "C) [MLT⁻¹]  (impuls)", "D) [ML²T⁻³]  (effekt)", "E) [T]  (tid)"],
        "correct": "B",
        "explain": "[h] = [E]/[f] = [ML²T⁻²]/[T⁻¹] = [ML²T⁻¹]. Samme dimension som impulsmoment (L=Iω) og virkning (action). h = 6.626×10⁻³⁴ J·s.",
    },

    # ── Skalering ──────────────────────────────────────────────────────────────
    {
        "emne": "Skalering",
        "q": "Fjedermasse-systemet T = 2π√(m/k). Hvis massen fordobles, hvad sker med perioden T?",
        "options": ["A) T fordobles (×2)", "B) T øges med faktor √2 ≈ 1.41", "C) T ændres ikke", "D) T halveres (÷2)", "E) T øges med faktor 4"],
        "correct": "B",
        "explain": "T ∝ √m. Fordobles m → T_ny = 2π√(2m/k) = √2·T_gammel. Generelt: T ∝ mⁿ, n=½. Kun kvadratroden af masse-ændringen overføres til perioden.",
    },
    {
        "emne": "Skalering",
        "q": "Keplers 3. lov: T² ∝ r³. En planet flyttes til tre gange sin nuværende afstand fra Solen. Hvad sker med dens omløbstid?",
        "options": ["A) T tredobles (×3)", "B) T øges med faktor 3² = 9", "C) T øges med faktor 3^(3/2) = 3√3 ≈ 5.20", "D) T øges med faktor √3 ≈ 1.73", "E) T ændres ikke"],
        "correct": "C",
        "explain": "T ∝ r^(3/2). Ny T = T_gammel·3^(3/2) = T·3·√3 ≈ 5.20·T. Jordmånen vs. jordbanen: r_jord ≈ 390× r_måne → T_jord ≈ 390^1.5 ≈ 7700× T_måne ≈ 365 dage ✓",
    },
    {
        "emne": "Skalering",
        "q": "Coulombs lov: F ∝ 1/r². To ladninger flyttes til det dobbelte af hinanden. Hvad sker med kraften?",
        "options": ["A) F halveres (×½)", "B) F falder til ¼", "C) F fordobles", "D) F ændres ikke", "E) F firedobles"],
        "correct": "B",
        "explain": "F ∝ r⁻². Ny F = F·(2r)⁻²/r⁻² = F·1/4. Eksponent er −2, så faktor 2 i r giver faktor 2⁻² = ¼ i F. Samme logik gælder tyngdekraften og elektrisk felt.",
    },
    {
        "emne": "Skalering",
        "q": "En satellit i lav kredsløb har v ∝ r^(-1/2) (v = √(GM/r)). Hvis radius fordobles, hvad sker med orbital­hastigheden?",
        "options": ["A) v fordobles", "B) v halveres", "C) v falder til v/√2 ≈ 0.71v", "D) v ændres ikke", "E) v øges med √2"],
        "correct": "C",
        "explain": "v ∝ r^(−½). Ny v = v·(2r)^(−½)/r^(−½) = v/√2 ≈ 0.71v. Bemærk: større kredsløb → lavere hastighed, men længere omløbstid. ISS har r≈6770 km, v≈7.7 km/s.",
    },
    {
        "emne": "Skalering",
        "q": "Elektrisk modstand: R = ρL/A. Hvis en leder gøres dobbelt så lang OG dobbelt så tyk i radius, hvad sker med R?",
        "options": ["A) R fordobles", "B) R halveres", "C) R ændres ikke", "D) R firedobles", "E) R falder til R/4"],
        "correct": "B",
        "explain": "A = πr² → fordobles r → A firedobles. R_ny = ρ·(2L)/(4A) = ½·(ρL/A) = R/2. Længde giver faktor 2 op, tværsnit (∝r²) giver faktor 4 ned → netto faktor ½.",
    },
    {
        "emne": "Skalering",
        "q": "Kinetisk energi Ek = ½mv². Hvis hastigheden tredobles (og massen er uændret), hvad sker med Ek?",
        "options": ["A) Ek tredobles", "B) Ek øges med faktor 6", "C) Ek øges med faktor 9", "D) Ek øges med faktor √3", "E) Ek fordobles"],
        "correct": "C",
        "explain": "Ek ∝ v². Ny Ek = ½m(3v)² = 9·½mv² = 9·Ek. Husk: i kollisioner og trafiksikkerhed er dette kritisk — tredoblet hastighed = ni gange så meget kinetisk energi der skal absorberes.",
    },
    # ── Dynamik: sløjfe og Newton ────────────────────────────────────────────────
    {
        "emne": "Dynamik",
        "q": "En lille klods starter fra hvile i højen h og ruller ned en friktionsfri bane ind i en lodret cirkulær sløjfe med radius r. Hvad er den mindste h for at klodsen gennemfører sløjfen?",
        "options": ["A) h = r", "B) h = 2r", "C) h = 2.5r", "D) h = 3r", "E) h = 5r"],
        "correct": "C",
        "explain": "I toppen kræves N ≥ 0, dvs. mv²/r ≥ mg → v_top ≥ √(gr). Energibevarelse: mgh = ½mv_top² + mg(2r) = ½mgr + 2mgr = (5/2)mgr → h_min = 5r/2 = 2.5r.",
    },
    {
        "emne": "Dynamik",
        "q": "En lastbil (5000 kg) kører ind i en personbil (1000 kg). Ifølge Newtons 3. lov: hvad er størelsesforholdet mellem kraften lastbilen udøver på personbilen og kraften personbilen udøver på lastbilen?",
        "options": ["A) 5:1 (lastbilen er tungere)", "B) 1:5 (personbilen oplever 5× mere)", "C) 1:1 (lige store og modsatrettede)", "D) Afhænger af hastighederne", "E) Afhænger af kollisionens varighed"],
        "correct": "C",
        "explain": "Newtons 3. lov: F₁₂ = −F₂₁ altid. Krafterne er altid ens store. Det er accelerationerne der er ulige: a = F/m, så personbilen (1000 kg) accelererer 5× så meget som lastbilen (5000 kg). Mange forveksler kraft og acceleration.",
    },
    # ── Termodynamik ─────────────────────────────────────────────────────────────
    {
        "emne": "Termodynamik",
        "q": "Et ideelt gas i et lukket beholder opvarmes fra 300 K til 1200 K (volumen konstant). Hvad sker med den kvadratiske middelhastighed v_rms af molekylerne?",
        "options": ["A) Fordobles — T er 4× større", "B) Firdobles — T er 4× større", "C) Øges med faktor 2 — T er 4× større, v_rms ∝ √T", "D) Øges med faktor √2", "E) Er uændret — volumen er konstant"],
        "correct": "C",
        "explain": "v_rms = √(3RT/M) ∝ √T. T øges med faktor 4 (fra 300 til 1200 K) → v_rms øges med √4 = 2. Dette er den klassiske eksamens­fælde: T fordobles → v_rms øges med √2, T firdobles → v_rms fordobles.",
    },
    {
        "emne": "Termodynamik",
        "q": "Idealgas gennemgår en adiabatisk kompression. Hvad gælder for temperatur og indre energi?",
        "options": ["A) T stiger, ΔU = Q = 0", "B) T stiger, ΔU = −W (W < 0 når gas komprimeres)", "C) T falder, da ingen varme tilføres", "D) T er uændret — adiabatisk", "E) ΔU = 0 uanset hvad"],
        "correct": "B",
        "explain": "Adiabatisk: Q = 0. 1. termodynamikslov: ΔU = Q − W = 0 − W = −W. Når gas komprimeres udføres arbejde PÅ gassen, dvs. W < 0 (gassen udfører negativt arbejde), og ΔU = −W > 0 → temperaturen stiger.",
    },
    # ── Kollisioner / Bølger ──────────────────────────────────────────────────────
    {
        "emne": "Kollisioner",
        "q": "En kugle (masse m) bevæger sig med fart v og støder ind i en identisk kugle (masse m) der hviler. Stødet er ELASTISK og centralt. Hvad sker der?",
        "options": ["A) Begge bevæger sig videre med v/2", "B) Den første standser, den anden bevæger sig videre med v", "C) Begge bevæger sig med v i vinkel 45°", "D) Den første bouncer tilbage med −v", "E) Ingen bevægelse — impuls annulleres"],
        "correct": "B",
        "explain": "Elastisk 1D med m₁=m₂: v₁' = (m₁−m₂)v/(m₁+m₂) = 0, v₂' = 2m₁v/(m₁+m₂) = v. Den første standser FULDSTÆNDIGT og overfører ALT impuls og AL kinetisk energi til den anden. Se fx Newton's vugge.",
    },
    {
        "emne": "Bølger",
        "q": "En ambulance kører mod dig med f=800 Hz. Hvad hører du sammenlignet med 800 Hz?",
        "options": ["A) Lavere frekvens — bølgerne trækkes ud", "B) Præcis 800 Hz — du er stationær", "C) Højere frekvens — bølgerne komprimeres foran kilden", "D) Afhænger af ambulancens masse", "E) Kun amplituden ændres, ikke frekvensen"],
        "correct": "C",
        "explain": "Doppler-effekt: f' = f·v/(v−v_s) > f når kilden nærmer sig (v_s > 0). Bølgefronterne 'presses' sammen foran kilden → kortere bølgelængde → højere frekvens. Når ambulancen er passeret: f' = f·v/(v+v_s) < f → lavere frekvens.",
    },

    # ── Rotation ──────────────────────────────────────────────────────────────────
    {
        "emne": "Rotation",
        "q": "En massiv cylinder og en tynd ring har samme masse m og radius r. Hvem accelererer hurtigst ned ad en skråning (ruller uden glidning)?",
        "options": ["A) Ringen — den er lettere ved kanten", "B) Cylinderen — I = ½mr² < mr²", "C) De accelererer ens — samme masse og radius", "D) Ringen — den har mere potentiel energi", "E) Afhænger af skråningens vinkel"],
        "correct": "B",
        "explain": "Acceleration a = g·sinθ/(1 + I/(mr²)). Cylinder: I=½mr² → a = g·sinθ/(1+½) = ⅔g·sinθ. Ring: I=mr² → a = g·sinθ/(1+1) = ½g·sinθ. Lavere I → mere kinetisk energi i translation → hurtigere. Massen falder ud.",
    },
    {
        "emne": "Rotation",
        "q": "En danseres arme trækkes ind mod kroppen mens hun snurrer frit (ingen ydre kraftmoment). Hvad sker med hendes vinkelhastighed?",
        "options": ["A) Falder — hun mister kinetisk energi", "B) Er uændret — ingen ydre kraftmoment", "C) Stiger — impulsmoment L = Iω er bevaret, I falder", "D) Stiger kun hvis hun trækker armene LANGSOMT ind", "E) Afhænger af armmassen"],
        "correct": "C",
        "explain": "L = Iω = konstant (intet ydre kraftmoment). Armene ind → I falder → ω stiger for at bevare L. Kinetisk energi Ek = L²/(2I) stiger faktisk — muskler udfører arbejde ved at trykke ind mod centrifugalkraften.",
    },
    {
        "emne": "Rotation",
        "q": "Hvad er Steiners sætning (parallelakseteoret)?",
        "options": ["A) I = ∫r² dm — definition af inertimoment", "B) I = I_cm + md² — inertimoment om parallel akse", "C) τ = Iα — rotationsanalog til F=ma", "D) L = Iω — impulsmoment", "E) I_total = I₁ + I₂ — sammensætning af inertimoment"],
        "correct": "B",
        "explain": "Steiners sætning: I_ny = I_cm + m·d², hvor d er afstanden fra massemidtpunktsaksens til den nye akse. I_cm er altid mindst — enhver anden parallel akse giver større I. Bruges når rotationscentret ikke er i massemidtpunktet.",
    },
    {
        "emne": "Rotation",
        "q": "En stang (masse m, længde L) roterer om sin ene ende. Hvad er dens inertimoment?",
        "options": ["A) mL²/12 (om midten)", "B) mL²/6", "C) mL²/3 (om enden)", "D) mL²/2", "E) mL²"],
        "correct": "C",
        "explain": "Om midten: I_cm = mL²/12. Om enden (afstand d = L/2 fra midten): Steiner → I = mL²/12 + m(L/2)² = mL²/12 + mL²/4 = mL²/3. Husk: om enden = 4× om midten.",
    },
    {
        "emne": "Rotation",
        "q": "Et hjul decelererer fra 300 RPM til 0 på 5 sekunder med konstant vinkelacceleration. Hvad er |α| (størrelsen af vinkelaccelerationen)?",
        "options": ["A) 60 rad/s²", "B) 6.28 rad/s²", "C) 3.14 rad/s²", "D) 10π/3 rad/s² ≈ 10.47 rad/s²", "E) 300 rad/s²"],
        "correct": "B",
        "explain": "ω₀ = 300·2π/60 = 10π rad/s ≈ 31.4 rad/s. α = (ω−ω₀)/t = (0−10π)/5 = −2π rad/s² ≈ −6.28 rad/s² (negativ da decelererende). |α| = 2π ≈ 6.28 rad/s². Husk at omregne RPM → rad/s: ω = RPM·2π/60.",
    },
    {
        "emne": "Rotation",
        "q": "En bold rulles (uden glidning) op ad en bakke. Hvor meget af den samlede kinetiske energi udgøres af rotation (massiv kugle, I = 2mr²/5)?",
        "options": ["A) 1/2 (50%)", "B) 2/7 ≈ 28.6%", "C) 1/3 (33.3%)", "D) 2/5 (40%)", "E) 1/7 ≈ 14.3%"],
        "correct": "B",
        "explain": "E_rot = ½Iω² = ½·(2mr²/5)·(v/r)² = mv²/5. E_trans = ½mv². E_total = ½mv² + mv²/5 = 7mv²/10. Andel = (mv²/5)/(7mv²/10) = (1/5)/(7/10) = 2/7 ≈ 28.6%. Resten (5/7) er translationsenergi.",
    },
    {
        "emne": "Rotation",
        "q": "To pladser er på et drejeplatform: A er 1 m fra centrum, B er 2 m fra centrum. Platformet roterer med konstant ω. Hvad gælder?",
        "options": ["A) A og B har samme lineær hastighed", "B) A og B har samme vinkelacceleration", "C) B har dobbelt så stor centripetalkraft som A (samme masse)", "D) B har dobbelt så stor vinkelhastighed", "E) A har større centripetalkraft end B"],
        "correct": "C",
        "explain": "v = ωr → v_B = 2v_A. F_c = mω²r → F_c,B = mω²·2r = 2·mω²·r = 2·F_c,A. Vinkelhastighed ω er ens for alle punkter på et fast legeme. Lineær hastighed og centripetalkraft er proportional med r.",
    },
    {
        "emne": "Rotation",
        "q": "En kugles inertimoment er I = 2mr²/5. Den er sat til at rotere om en akse der tangerer overfladen. Find I om denne akse.",
        "options": ["A) 2mr²/5", "B) 3mr²/5", "C) 7mr²/5", "D) mr²", "E) 5mr²/2"],
        "correct": "C",
        "explain": "Steiner: d = r (afstand fra centrum til tangentakse). I = I_cm + mr² = 2mr²/5 + mr² = 2mr²/5 + 5mr²/5 = 7mr²/5.",
    },

    # ── Svingninger ───────────────────────────────────────────────────────────────
    {
        "emne": "Svingninger",
        "q": "Et fjedermasse-system har T = 2 s. Hvad sker med perioden hvis massen fordobles OG fjederkonstanten halveres?",
        "options": ["A) T fordobles til 4 s", "B) T er uændret", "C) T firedobles til 8 s", "D) T øges med faktor √2 til 2.83 s", "E) T tredobles til 6 s"],
        "correct": "A",
        "explain": "T = 2π√(m/k). Ny T' = 2π√(2m/(k/2)) = 2π√(4m/k) = 2·2π√(m/k) = 2T = 4 s. Fordoblet m giver faktor √2 opad, halveret k giver yderligere faktor √2 opad → samlet faktor 2.",
    },
    {
        "emne": "Svingninger",
        "q": "Et simpelt pendul svinger med T = 2 s på Jorden (g = 9.82 m/s²). Hvor lang er pendlet?",
        "options": ["A) L ≈ 0.5 m", "B) L ≈ 0.99 m (≈ 1 m)", "C) L ≈ 2 m", "D) L ≈ 4 m", "E) Afhænger af masse"],
        "correct": "B",
        "explain": "T = 2π√(L/g) → L = g·T²/(4π²) = 9.82·4/(4π²) = 39.28/39.48 ≈ 0.994 m. Et sekundpendul (T=2 s) har L ≈ 1 m — dette er faktisk definitionen af 'en meter' historisk set!",
    },
    {
        "emne": "Svingninger",
        "q": "En harmonisk oscillator starter ved x = A (fuld amplitude, v = 0). Hvornår er den kinetiske energi lig den potentielle energi?",
        "options": ["A) Aldrig — de veksler asymmetrisk", "B) Kun i x = 0", "C) Ved x = A/√2 (≈ 0.707A)", "D) Ved x = A/2", "E) Afhænger af fjederkonstanten"],
        "correct": "C",
        "explain": "Ek = Ep: ½mv² = ½kx². Total E = ½kA². Ek = ½k(A²−x²), Ep = ½kx². Ek = Ep → A²−x² = x² → x = A/√2. Bemærk: dette er IKKE ved x = A/2. Mange forveksler dette.",
    },
    {
        "emne": "Svingninger",
        "q": "Hvad er resonans i et dæmpet svingningssystem?",
        "options": ["A) Systemet svinger med maksimal frekvens", "B) Dæmpningskonstanten er nul", "C) Amplitude er maksimal når ω_drive ≈ ω₀ (egenfrekvens)", "D) Svingningen stopper pludseligt", "E) Frekvensen dobbelt sig"],
        "correct": "C",
        "explain": "Resonans opstår når pådrivningsfrekvensen ω nærmer sig egenfrekvensen ω₀ = √(k/m). Amplituden er maksimal ved resonans. Jo lavere dæmpning, desto skarpere og højere resonanspeak. Bruges i MR-scanning, brodesign (undgå!), musikinstrumenter.",
    },
    {
        "emne": "Svingninger",
        "q": "To fjedre med k₁ = k₂ = 100 N/m kobles i serie. Hvad er den effektive fjederkonstant?",
        "options": ["A) 200 N/m", "B) 100 N/m", "C) 50 N/m", "D) 141 N/m", "E) 70.7 N/m"],
        "correct": "C",
        "explain": "Serie: 1/k_eff = 1/k₁ + 1/k₂ = 1/100 + 1/100 = 2/100 → k_eff = 50 N/m. Serie giver blødere fjeder (lavere k). Parallel: k_eff = k₁ + k₂ = 200 N/m (stivere). Serie og parallel er modsat hinanden ift. modstande!",
    },
    {
        "emne": "Svingninger",
        "q": "Et simpelt pendul svinger med amplitude 5°. Fordobles amplituden til 10°. Hvad sker med perioden?",
        "options": ["A) T fordobles", "B) T øges med √2", "C) T er (næsten) uændret — gælder for små vinkler", "D) T halveres", "E) T afhænger af amplitude — ingen klar regel"],
        "correct": "C",
        "explain": "T = 2π√(L/g) er uafhængig af amplitude for KLEINE vinkler (< ~15°). Begge vinkler er inden for det lineære regime. For store vinkler er der en lille korrektion, men den er negligibel her. Pendlets periode afhænger af L og g, ikke amplitude.",
    },
    {
        "emne": "Svingninger",
        "q": "En masse på en fjeder: v = 0 ved x = +A og x = −A. Hvad er v i x = 0?",
        "options": ["A) v = 0 altid", "B) v = A·ω (maksimal)", "C) v = A·ω/2", "D) v = √(kA²/m)", "E) B og D er ens — begge korrekte"],
        "correct": "E",
        "explain": "v_max = A·ω = A·√(k/m). Fra energibevarelse: ½mv_max² = ½kA² → v_max = A√(k/m) = Aω. Begge svar er korrekte og ækvivalente. v_max opstår i ligevægtspositionen x = 0 hvor al energi er kinetisk.",
    },

    # ── Relativitetsteori ─────────────────────────────────────────────────────────
    {
        "emne": "Relativitetsteori",
        "q": "En raket rejser forbi Jorden med v = 0.8c. Hvad er Lorentz-faktoren γ?",
        "options": ["A) γ = 0.6", "B) γ = 0.8", "C) γ = 1.25", "D) γ = 1.67", "E) γ = 2.0"],
        "correct": "D",
        "explain": "γ = 1/√(1−v²/c²) = 1/√(1−0.64) = 1/√0.36 = 1/0.6 = 5/3 ≈ 1.667. Husk: γ ≥ 1 altid, og γ → ∞ når v → c. ved v = 0.8c: √(1−0.64) = √0.36 = 0.6, ikke 0.8.",
    },
    {
        "emne": "Relativitetsteori",
        "q": "Et ur om bord på en raket (v = 0.6c) tæller 10 s. Hvad registrerer en stationær observatør?",
        "options": ["A) 8 s (kortere — bevægelse forkurter tid)", "B) 10 s (uændret)", "C) 12.5 s (længere — tidsudvidelse)", "D) 6 s", "E) Afhænger af om raketten accelererer"],
        "correct": "C",
        "explain": "γ = 1/√(1−0.36) = 1/0.8 = 1.25. Stationær tid Δt = γ·Δt₀ = 1.25·10 = 12.5 s. Bevægende ure GÅR LANGSOMMERE set fra en stationær observatør. Δt₀ er egentid (målt i rakettens referencesystem).",
    },
    {
        "emne": "Relativitetsteori",
        "q": "Et tog med hvilelængde L₀ = 100 m bevæger sig med v = 0.8c. Hvad er togenes observerede længde for en stationær person?",
        "options": ["A) 100 m (uændret)", "B) 80 m", "C) 60 m", "D) 125 m", "E) 166.7 m"],
        "correct": "C",
        "explain": "Længdekontraktion: L = L₀/γ = 100/1.667 = 60 m. Objekter kontraheres i bevægelsesretningen. γ = 1/√(1−0.64) = 1/0.6 = 5/3. L = 100·0.6 = 60 m. Kun i bevægelsesretningen — tværgående dimensioner er uændrede.",
    },
    {
        "emne": "Relativitetsteori",
        "q": "Hvad er hvilemasse­energien for en elektron (m_e = 9.11×10⁻³¹ kg)?",
        "options": ["A) 8.19×10⁻¹⁴ J = 0.511 MeV", "B) 1.60×10⁻¹⁹ J = 1 eV", "C) 938 MeV (protonenergi)", "D) 0 — elektroner er masseløse", "E) 1 J"],
        "correct": "A",
        "explain": "E₀ = m_e·c² = 9.11×10⁻³¹·(3×10⁸)² = 8.20×10⁻¹⁴ J. I eV: 8.20×10⁻¹⁴/1.602×10⁻¹⁹ = 511 000 eV = 0.511 MeV. Dette er et vigtigt grundtal i partikel­fysik.",
    },
    {
        "emne": "Relativitetsteori",
        "q": "Kan to partikler, der begge bevæger sig med 0.7c (men i modsatte retninger), 'se' hinanden med en relativ hastighed større end c?",
        "options": ["A) Ja, relativ hastighed = 1.4c", "B) Nej, relativistisk hastighedsaddition giver v_rel < c", "C) Kun hvis de har forskellige masser", "D) Ja, op til 2c er tilladt", "E) Spørgsmålet giver ikke mening"],
        "correct": "B",
        "explain": "Relativistisk hastighedsaddition: v_rel = (v₁+v₂)/(1+v₁v₂/c²) = (0.7+0.7)c/(1+0.49) = 1.4c/1.49 ≈ 0.94c. Altid < c. Klassisk ville give 1.4c, men det er forkert. Ingenting kan overskride lyshastighed i noget referencesystem.",
    },
    {
        "emne": "Relativitetsteori",
        "q": "En partikel har kinetisk energi Ek = 3m₀c². Hvad er dens totale energi E?",
        "options": ["A) E = 3m₀c²", "B) E = 4m₀c²", "C) E = √10·m₀c²", "D) E = 3.5m₀c²", "E) E = 9m₀c²"],
        "correct": "B",
        "explain": "E_total = E_hvilemasse + Ek = m₀c² + 3m₀c² = 4m₀c². Eller: E = γm₀c² → γ = 4. Kinetisk energi i relativitetsteori: Ek = (γ−1)m₀c², ikke ½mv².",
    },
    {
        "emne": "Relativitetsteori",
        "q": "Hvornår er den relativistiske kinetisk energi Ek = (γ−1)m₀c² en god approksimation til ½mv²?",
        "options": ["A) Aldrig — de er altid forskellige", "B) Kun for masseløse partikler", "C) Når v << c (ikke-relativistisk grænse)", "D) Når v = c/2", "E) Kun for elektroner"],
        "correct": "C",
        "explain": "For v << c: γ ≈ 1 + v²/(2c²), så Ek = (γ−1)m₀c² ≈ ½m₀v². Den klassiske formel er en approksimation der er valid når v/c << 1 (typisk < 1%). For daglige hastigheder er fejlen negligibel.",
    },

    # ── Energi ────────────────────────────────────────────────────────────────────
    {
        "emne": "Energi",
        "q": "En klods (m=2 kg) trykkes 10 cm ind i en fjeder (k=500 N/m) og slippes. Hvad er klodsen hastighed når fjederen er i naturlig længde?",
        "options": ["A) 0.5 m/s", "B) 1.0 m/s", "C) 1.58 m/s", "D) 2.24 m/s", "E) 5.0 m/s"],
        "correct": "C",
        "explain": "Energibevarelse: ½kx² = ½mv². v = x·√(k/m) = 0.10·√(500/2) = 0.10·√250 = 0.10·15.81 = 1.581 m/s. Alternativt: v = Aω = A·√(k/m) — det er SHM-sammenhængen.",
    },
    {
        "emne": "Energi",
        "q": "Hvad er effektiviteten af en ideel Carnot-maskine der arbejder mellem Tv = 600 K og Tk = 300 K?",
        "options": ["A) 100% — ideel maskine", "B) 75%", "C) 50%", "D) 25%", "E) Afhænger af kølemiddel"],
        "correct": "C",
        "explain": "η_Carnot = 1 − Tk/Tv = 1 − 300/600 = 1 − 0.5 = 50%. Ingen virkelig maskine kan nå 100%. Carnot-effektiviteten er den teoretisk maksimale — uanset konstruktion. Vigtig: brug altid KELVIN, ikke Celsius!",
    },
    {
        "emne": "Energi",
        "q": "En bold kastes op med starthastighed v₀. Hvad er boldens mekaniske energi i toppunktet (ingen luftmodstand)?",
        "options": ["A) 0 — al kinetisk energi er tabt", "B) ½mv₀² (bevaret)", "C) mgh_max (kun potentiel)", "D) B og C er ens — begge korrekte", "E) Afhænger af masse"],
        "correct": "D",
        "explain": "Mekanisk energi bevares: E_total = ½mv₀² = mgh_max. I toppunktet er al energi potentiel: E = mgh_max = ½mv₀². Begge udtryk er ens og korrekte. Vælg det der er nemmest at bruge i den konkrete opgave.",
    },
    {
        "emne": "Energi",
        "q": "Hvad gælder for effekten P = dW/dt ved konstant hastighed v mod en konstant kraft F?",
        "options": ["A) P = F²/v", "B) P = F·v", "C) P = ½mv²/t", "D) P = F·v²", "E) P = 0 da acceleration er nul"],
        "correct": "B",
        "explain": "P = dW/dt = F·ds/dt = F·v. Ved konstant v og konstant F (fx bil i konstant fart): P = F·v. Eksempel: bil 1000 N modstand, 30 m/s → P = 30 kW. Acceleration er nul, men motoren udfører stadig arbejde mod modstanden.",
    },
    {
        "emne": "Energi",
        "q": "En pendul svinger i luftmodstand (dæmpet). Hvad sker med dens mekaniske energi over tid?",
        "options": ["A) Bevares — energibevarelse gælder altid", "B) Forøges — luften tilføjer energi", "C) Falder — energi dissiperes til varme", "D) Bevares hvis svingningsamplituden er lille", "E) Fluktuerer op og ned"],
        "correct": "C",
        "explain": "Med luftmodstand (ikke-konservativ kraft) bevares mekanisk energi IKKE. Energi overføres til termisk energi i luften. Amplitude falder eksponentielt: A(t) = A₀·e^(−bt/2m). Total energi E = E₀·e^(−bt/m) falder kontinuerligt.",
    },

    # ── Elektricitet ──────────────────────────────────────────────────────────────
    {
        "emne": "Elektricitet",
        "q": "Tre modstande R₁=R₂=R₃=6Ω er koblet i parallelforbindelse. Hvad er den samlede modstand?",
        "options": ["A) 18 Ω", "B) 6 Ω", "C) 3 Ω", "D) 2 Ω", "E) 1 Ω"],
        "correct": "D",
        "explain": "Parallel: 1/R = 1/6 + 1/6 + 1/6 = 3/6 = 1/2 → R = 2Ω. For n identiske modstande R i parallel: R_eff = R/n = 6/3 = 2Ω. Parallelforbindelses samlede modstand er ALTID mindre end den mindste enkeltmodstand.",
    },
    {
        "emne": "Elektricitet",
        "q": "En kondensator C er ladet til spænding U. Hvad er den lagrede energi?",
        "options": ["A) E = CU", "B) E = ½CU", "C) E = ½CU²", "D) E = CU²", "E) E = C²U"],
        "correct": "C",
        "explain": "E = ½CU² = ½Q²/C = Q²/(2C). Faktoren ½ skyldes at ladningen opbygges gradvist — man kan ikke blot gange Q med U, da U varierer under opladningen. Sammenlign: ½kx² for fjeder, ½mv² for kinetisk energi.",
    },
    {
        "emne": "Elektricitet",
        "q": "Et elektron (q = −e) bevæger sig ind i et magnetfelt B vinkelret på sin bevægelsesvej. Hvad sker der?",
        "options": ["A) Elektronens fart aftager", "B) Elektronen bevæger sig i en ret linje", "C) Elektronen bevæger sig i en cirkel med konstant fart", "D) Elektronen accelereres parallelt med B", "E) Elektronen stopper"],
        "correct": "C",
        "explain": "Lorentz-kraften F = qv×B er altid vinkelret på v → ingen arbejde → fart konstant. Kraften er centripetal → cirkulær bevægelse. Radius: r = mv/(|q|B). For elektroner: meget lille radius pga. lille masse. Bruges i massespektrometer og cyklotroner.",
    },
    {
        "emne": "Elektricitet",
        "q": "Ohms lov gælder for en resistor. Fordobles spændingen U over resistoren, hvad sker med effektforbruget P?",
        "options": ["A) P fordobles", "B) P firedobles", "C) P halveres", "D) P er uændret", "E) P øges med √2"],
        "correct": "B",
        "explain": "P = U²/R. Fordobles U: P_ny = (2U)²/R = 4U²/R = 4P. Kvadratisk sammenhæng! Alternativt: P = UI = U·(U/R) = U²/R. Vigtig i elinstallation: dobbelt spænding = fire gange varmeudvikling.",
    },
    {
        "emne": "Elektricitet",
        "q": "Hvad er den elektriske feltstyrke E midt imellem to parallelle plader (+Q og −Q) med areal A og afstand d?",
        "options": ["A) E = Q/(ε₀A), rettet fra + til −", "B) E = Q·d/(ε₀A)", "C) E = 0 midt imellem", "D) E = kQ/d²", "E) E = Q/(2ε₀A) fra hver plade"],
        "correct": "A",
        "explain": "For parallelplader: E = σ/ε₀ = Q/(ε₀A), jævnt fordelt og rettet fra + til −. Feltet UDENFOR pladerne er (næsten) nul. Spænding: U = E·d = Qd/(ε₀A). Kapacitans: C = Q/U = ε₀A/d.",
    },

    # ── Bølger ────────────────────────────────────────────────────────────────────
    {
        "emne": "Bølger",
        "q": "Et lys med λ = 500 nm går fra luft ind i glas med n = 1.5. Hvad sker med bølgelængde og frekvens?",
        "options": ["A) Begge ændres", "B) Begge er uændret", "C) λ falder til 333 nm, f er uændret", "D) f falder, λ er uændret", "E) λ stiger, f falder"],
        "correct": "C",
        "explain": "f er bestemt af kilden og ændres ikke (hvad enten lys passerer grænse). λ = v/f, og v_glas = c/n = c/1.5. Ny λ = λ_luft/n = 500/1.5 = 333 nm. v og λ ændres — f bevares. Dette er analogt til lydbølger der passerer fra luft til vand.",
    },
    {
        "emne": "Bølger",
        "q": "En stående bølge på en streng (fasthæftet i begge ender, L = 60 cm) svinger i 3. harmoniske. Hvad er bølgelængden?",
        "options": ["A) λ = 120 cm", "B) λ = 60 cm", "C) λ = 40 cm", "D) λ = 30 cm", "E) λ = 20 cm"],
        "correct": "C",
        "explain": "For n-te harmoniske: L = n·λ/2 → λ = 2L/n. N=3: λ = 2·60/3 = 40 cm. 1. harmoniske (grundtone): λ = 120 cm. 2. harmoniske: λ = 60 cm. 3. harmoniske: λ = 40 cm. Antallet af buer = n.",
    },
    {
        "emne": "Bølger",
        "q": "Youngs dobbeltspalteforsøg: afstanden mellem spalter fordobles (d→2d), alt andet uændret. Hvad sker med afstanden mellem maksima på skærmen?",
        "options": ["A) Dobbelt afstand", "B) Halveret afstand", "C) Uændret", "D) Fire gange afstand", "E) √2 gange afstand"],
        "correct": "B",
        "explain": "y_m = mλL/d. Fordobles d: y_m' = mλL/(2d) = y_m/2. Tættere spalter → wider interferensmønster; bredere spalter → snævrere mønster. Omvendt proportionalt.",
    },

    # ── Atomfysik ─────────────────────────────────────────────────────────────────
    {
        "emne": "Atomfysik",
        "q": "Hvad er halvlevetiden for et stof hvis efter 3 halvlevetider er 12.5% tilbage?",
        "options": ["A) Dette er inkonsistent — det burde være 25%", "B) Det stemmer — 12.5% = (½)³ = ½³", "C) Der er gået 4 halvlevetider", "D) Afhænger af det specifikke stof", "E) T½ = 3 × den observerede tid"],
        "correct": "B",
        "explain": "N/N₀ = (½)^n, n = antal halvlevetider. (½)³ = 1/8 = 12.5%. Det stemmer perfekt med 3 halvlevetider. Den samlede tid er 3·T½. Eksempel: T½ = 10 år → 30 år → 12.5% tilbage.",
    },
    {
        "emne": "Atomfysik",
        "q": "En foton har energi E = 3 eV. Hvad er dens bølgelængde?",
        "options": ["A) λ ≈ 100 nm (ultraviolet)", "B) λ ≈ 414 nm (violet synligt lys)", "C) λ ≈ 620 nm (rødt lys)", "D) λ ≈ 1000 nm (infrarødt)", "E) λ ≈ 0.1 nm (røntgen)"],
        "correct": "B",
        "explain": "λ = hc/E. E = 3 eV = 3·1.602×10⁻¹⁹ = 4.81×10⁻¹⁹ J. λ = (6.626×10⁻³⁴·3×10⁸)/(4.81×10⁻¹⁹) = 4.13×10⁻⁷ m ≈ 413 nm. Violet synligt lys (380-450 nm). Husk: synligt lys 400-700 nm, 3 eV ≈ violet.",
    },
]

EKSAMENSTRAP = [
    {
        "trap": "Kelvin vs. Celsius i gasformler",
        "fejl": "pV = nRT med T i Celsius → alt for småt resultat eller division med ca. 20 i stedet for 293.",
        "ret": "T i formler er ALTID Kelvin. K = °C + 273.15. Typisk stuetemperatur: 20°C = 293.15 K.",
        "emne": "Termodynamik",
    },
    {
        "trap": "km/h vs. m/s i kinematik",
        "fejl": "Indsæt 90 i SUVAT i stedet for 25 m/s → bremseafstand 11× for stor.",
        "ret": "v [m/s] = v [km/h] / 3.6. Eksamen angiver gerne km/h. Tjek altid enheder FØR beregning.",
        "emne": "Kinematik",
    },
    {
        "trap": "Glemme rotationsenergi ved rulning",
        "fejl": "Brug kun E_kin = ½mv² for en rullende bold/cylinder — ignorerer ½Iω².",
        "ret": "Rulning: E_total = ½mv² + ½Iω² = ½mv²(1 + I/(mr²)). Kugle: faktor 7/5, cylinder: faktor 3/2.",
        "emne": "Rotation",
    },
    {
        "trap": "v_rms skalerer med √T, ikke T",
        "fejl": "T fordobles → v_rms fordobles. Forkert! v_rms ∝ √T.",
        "ret": "v_rms = √(3RT/M). T×4 → v_rms×2. T×2 → v_rms×√2 ≈ 1.41. Eksamen tester dette direkte.",
        "emne": "Termodynamik",
    },
    {
        "trap": "Centripetalkraft som 'ekstra kraft'",
        "fejl": "Tegne centripetalkraft F_c som en selvstændig pil på kraftdiagrammet.",
        "ret": "F_c = mv²/r er NETTOKRAFTEN mod centrum — summen af alle reelle kræfter. Ikke en ny kraft.",
        "emne": "Dynamik",
    },
    {
        "trap": "Bremseafstand ∝ v² (ikke v)",
        "fejl": "Fordoblet hastighed → fordoblet bremseafstand.",
        "ret": "s = v₀²/(2a) ∝ v₀². Fordoblet v₀ → firedoblet bremseafstand! Det er derfor 130 km/h er farligere end 90 km/h.",
        "emne": "Kinematik",
    },
    {
        "trap": "Statisk friktion er IKKE altid μ_s·N",
        "fejl": "Sætte f = μ_s·N selvom legemet er i hvile under en lille kraft.",
        "ret": "Statisk friktion matcher den påvirkte kraft: f = F_ydre (op til μ_s·N). Kun VED grænsen er f = μ_s·N.",
        "emne": "Dynamik",
    },
    {
        "trap": "Energi/effekt i kondensator: E = ½CU², ikke CU",
        "fejl": "E = CU (mangler faktor ½).",
        "ret": "E = ½CU² = Q²/(2C). Faktoren ½ skyldes gradvis opladning — parallelt med ½kx² (fjeder) og ½mv².",
        "emne": "Elektricitet",
    },
    {
        "trap": "Tidsudvidelse: bevægende ur GÅR LANGSOMT",
        "fejl": "Tro at γ komprimerer (forkorter) den observerede tid.",
        "ret": "Δt = γ·Δt₀ ≥ Δt₀. Stationær observatør måler LÆNGERE tid. Bevægende ure tikker langsommere.",
        "emne": "Relativitetsteori",
    },
    {
        "trap": "h_min for loop = 2.5r, ikke 2r",
        "fejl": "h_min = 2r (sætte al energi til potentiel energi i toppen, glemme kinetisk energi i toppen).",
        "ret": "I toppen kræves v_top ≥ √(gr) (N≥0). Energibevarelse: mgh = ½m(gr) + mg(2r) → h = 5r/2 = 2.5r.",
        "emne": "Dynamik",
    },
]

# ── Faner: Spørgsmål / Eksamenstrap ───────────────────────────────────────────
_emne_filter_now = st.session_state.get("teori_emne", "Alle")
_filtrerede_count = len(QUESTIONS) if _emne_filter_now == "Alle" else sum(1 for q in QUESTIONS if q["emne"] == _emne_filter_now)
tab_spg, tab_trap = st.tabs([f"🧠 Spørgsmål ({_filtrerede_count})", "⚠️ Eksamenstrap (top 10)"])

with tab_spg:
    EMNER = ["Alle"] + sorted(list({q["emne"] for q in QUESTIONS}))
    emne_filter = st.radio("Vis emne:", EMNER, horizontal=True, key="teori_emne")

    filtrerede = QUESTIONS if emne_filter == "Alle" else [q for q in QUESTIONS if q["emne"] == emne_filter]

    if "teori_revealed" not in st.session_state:
        st.session_state["teori_revealed"] = set()

    _q_global_idx = {id(q): i for i, q in enumerate(QUESTIONS)}

    n_revealed = sum(
        1 for q in filtrerede
        if f"q_{_q_global_idx[id(q)]}" in st.session_state["teori_revealed"]
    )

    col_info, col_reset = st.columns([6, 1])
    col_info.markdown(f"**{len(filtrerede)} spørgsmål** — {n_revealed} svar åbnet")
    if col_reset.button("↺ Nulstil", use_container_width=True):
        st.session_state["teori_revealed"] = set()
        st.rerun()

    st.divider()

    for i, q in enumerate(filtrerede):
        q_id = f"q_{_q_global_idx[id(q)]}"
        revealed = q_id in st.session_state["teori_revealed"]

        header = f"{'✅ ' if revealed else ''}{i+1}. **[{q['emne']}]** {q['q']}"
        with st.expander(header, expanded=False):
            for opt in q["options"]:
                st.markdown(f"- {opt}")

            st.divider()
            if not revealed:
                if st.button("Vis svar", key=f"teori_btn_{q_id}", type="primary"):
                    st.session_state["teori_revealed"].add(q_id)
                    st.rerun()
            else:
                correct_opt = next(
                    (o for o in q["options"] if o.startswith(q["correct"] + ")")),
                    q["correct"],
                )
                st.success(f"✅ **{correct_opt}**")
                st.info(f"💡 {q['explain']}")

with tab_trap:
    st.markdown("De **10 hyppigste fejl** på DTU 10060 eksamen. Læs dem aftenen før — 10 minutter der kan redde karakteren.")
    st.divider()

    TRAP_EMNE_FILTER = ["Alle"] + sorted(list({t["emne"] for t in EKSAMENSTRAP}))
    trap_filter = st.radio("Emne:", TRAP_EMNE_FILTER, horizontal=True, key="trap_emne")
    filtrerede_trap = EKSAMENSTRAP if trap_filter == "Alle" else [t for t in EKSAMENSTRAP if t["emne"] == trap_filter]

    for t in filtrerede_trap:
        with st.container(border=True):
            st.markdown(f"**⚠️ {t['trap']}** `[{t['emne']}]`")
            st.error(f"❌ **Typisk fejl:** {t['fejl']}")
            st.success(f"✅ **Korrekt:** {t['ret']}")
