class Rektangel:
    # Jeg fjernet variablene a og b ettersom disse ikke er brukt i programmet. 

    # Det er god sikk å kalde den første parameteren (som er en referanse til dette objektet / seg selv) for self. 
    # Her er det også nødvendig ettersom vi sier self.side1 og self.side2. Vi kunne ha valgt å endre self.side1 og self.side2 til selve_objektet.side1 
    # og selve_objektet.side2, men det er som sagt god sikk å kalle denne variablen for self. 
    def __init__(self, side1: float = 1.0, side2: float = 1.0):
        """Rektangel tar to argumenter for side 1 og side 2. Dette er høyden og bredden til rektangelet. """
        self.side1 = side1
        self.side2 = side2


    # Vi må legge til self som den første variablen ettersom ellers ville programmet ganget seg selv (kalt seg selv for "lengde") 
    # med et tall bredde, som ikke gir så mye mening. Det gir heller ikke så mye mening å ha variablene lengde og bredde ettersom vi regner 
    # arealet av en rektangel og vi allerede har fått vite lengden på side 1 og side 2 i __init__ og lagret de internt i objektet. 
    # Jeg fjerner derfor disse paramterne og sier isteden self.side1 * self*side2
    def beregne_areal(self):
        """
        Regner ut arealet til rektangelet. Tar ingen paramterere. Bruker formelen høyde * bredde = areal (her side1 * side2 = areal).
        Du kan endre lengdene på sidene til rektangelet ved bruk av (objekt).side1 = x1 og (objekt).side2 = x2
        """
        return self.side1*self.side2
    
# Erstatter variablen hest med et vilkårlig tall
firkant = Rektangel(2.1, 17.9)
