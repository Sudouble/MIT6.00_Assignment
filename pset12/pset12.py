# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab
import matplotlib.pyplot as plt
import copy


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """


#
# PROBLEM 1
#

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """

    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step.

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        if random.random() < self.clearProb:
            return True
        return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        if random.random() < self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            return NoChildException("No Child")


class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):
        """
        Gets the current total virus population.

        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.

        returns: the total virus population at the end of the update (an
        integer)
        """
        tmpViruses = []
        for virus in self.viruses:
            # print virus
            if virus.doesClear():
                self.viruses.remove(virus)
            density = len(self.viruses) / 1.0 / self.maxPop
            re_val = virus.reproduce(density)
            if type(re_val) == SimpleVirus:
                tmpViruses.append(re_val)
        tmpViruses.extend(self.viruses)
        self.viruses = tmpViruses
        return len(self.viruses)


#
# PROBLEM 2
#

def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.
    """
    viruses = []
    maxBirthProb = 0.1
    clearProb = 0.05
    for i in range(100):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))
    patient = SimplePatient(viruses, 1000)

    trail_time = 300

    size_ = []
    for gen in xrange(trail_time):
        size_.append(patient.update())

    pylab.plot(xrange(trail_time), size_)
    pylab.xlabel("size")
    pylab.ylabel("Population")
    pylab.title("12...")
    pylab.show()


# problem2()

#
# PROBLEM 3
#

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        # self.maxBirthProb = maxBirthProb
        # self.clearProb = clearProb
        self.resistance = resistances
        self.mutProb = mutProb

    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistance.get(drug, False)

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        for drug in activeDrugs:
            if not self.getResistance(drug):
                return NoChildException("No Child")

        reproduce = self.maxBirthProb * (1 - popDensity)
        if random.random() < reproduce:
            result = ResistantVirus(self.maxBirthProb, self.clearProb, copy.deepcopy(self.resistance), self.mutProb)

            prob_le = random.random() < self.mutProb
            for d_drug in self.resistance:
                if prob_le:
                    # result.resistance[d_drug] = not result.resistance[d_drug]
                    if result.getResistance(d_drug):
                        result.resistance[d_drug] = False
                    else:
                        result.resistance[d_drug] = True
                else:
                    result.resistance[d_drug] = self.resistance[d_drug]
            return result
        else:
            return NoChildException("No Child")

class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.newDrugs = set()

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        self.newDrugs.add(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return list(self.newDrugs)

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count = 0
        for virus in self.viruses:
            for resist in drugResist:
                if not virus.getResistance(resist):
                    break
            else:
                count += 1
        return count

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: the total virus population at the end of the update (an
        integer)
        """
        tmp_viruses = []
        pop_density = len(self.viruses) / 1.0 / self.maxPop
        for virus in self.viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
            else:
                if type(virus) == SimpleVirus:
                    re_val = virus.reproduce(pop_density)
                    # print "virus"
                else:
                    re_val = virus.reproduce(pop_density, self.newDrugs)
                    # print type(re_val)
                if not type(re_val) == NoChildException:
                    tmp_viruses.append(re_val)
        tmp_viruses.extend(self.viruses)
        self.viruses = tmp_viruses
        return len(self.viruses)


#
# PROBLEM 4
#

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    maxBirthProb = 0.1
    clearProb = 0.05
    maxPop = 1000
    mutProb = 0.005
    resitances = {'guttagonol': False}

    viruses = []
    for i in range(100):
        resist_virus = ResistantVirus(maxBirthProb, clearProb, resitances, mutProb)
        viruses.append(resist_virus)

    patient = Patient(viruses, maxPop)

    trail_time = 300
    size_ = []
    resist_size = []
    for gen in xrange(trail_time):
        size_.append(patient.update())
        if gen == 150:
            patient.addPrescription('guttagonol')
        resist_size.append(patient.getResistPop(['guttagonol']))

    pylab.plot(xrange(trail_time), resist_size)
    pylab.plot(xrange(trail_time), size_)
    pylab.xlabel("size")
    pylab.ylabel("Population")
    pylab.title("virus population iteration")
    pylab.show()


# problem4()

#
# PROBLEM 5
#

def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).
    """
    maxBirthProb = 0.1
    clearProb = 0.05
    maxPop = 1000
    mutProb = 0.005
    resitances = {'guttagonol': False}

    trail_times = [300, 150, 75, 0]
    result = []
    for trail_time in trail_times:
        viruses = []
        for i in range(100):
            resist_virus = ResistantVirus(maxBirthProb, clearProb, resitances, mutProb)
            viruses.append(resist_virus)

        patient = Patient(viruses, maxPop)
        size_ = []
        for gen in xrange(trail_time):
            size_.append(patient.update())

        for treat_time in xrange(150):
            patient.addPrescription('guttagonol')
            size_.append(patient.update())

        result.append(size_[-1])
    print result

    name_list = ['300', '150', '75', '0']
    plt.bar(range(len(result)), result, tick_label=name_list)
    plt.show()

# problem5()

#
# PROBLEM 6
#

def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    maxBirthProb = 0.1
    clearProb = 0.05
    maxPop = 1000
    mutProb = 0.005
    resitances = {'guttagonol': False, 'grimpex': False}

    trail_times = [300, 150, 75, 0]
    for trail_time in trail_times:
        result = []
        for repeat in range(30):
            viruses = []
            for i in range(100):
                resist_virus = ResistantVirus(maxBirthProb, clearProb, resitances, mutProb)
                viruses.append(resist_virus)

            patient = Patient(viruses, maxPop)

            size_ = []
            # stage 1
            for gen in xrange(150):
                size_.append(patient.update())
            patient.addPrescription('guttagonol')
            # stage 2
            for gen in xrange(trail_time):
                size_.append(patient.update())
            patient.addPrescription('grimpex')
            # stage 3
            for treat_time in xrange(150):
                size_.append(patient.update())
            result.append(size_[-1])

        plt.figure()
        plt.bar(range(len(result)), result)
        plt.title(str(trail_time))

    plt.show()

# problem6()

#
# PROBLEM 7
#

def problem7():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.
    """
    maxBirthProb = 0.1
    clearProb = 0.05
    maxPop = 1000
    mutProb = 0.005
    resitances = {'guttagonol': False, 'grimpex': False}

    trail_times = [300]
    result = []
    for trail_time in trail_times:
        viruses = []
        for i in range(100):
            resist_virus = ResistantVirus(maxBirthProb, clearProb, resitances, mutProb)
            viruses.append(resist_virus)

        patient = Patient(viruses, maxPop)

        size_ = []
        # stage 1
        for gen in xrange(150):
            size_.append(patient.update())
        patient.addPrescription('guttagonol')
        # stage 2
        for gen in xrange(trail_time):
            size_.append(patient.update())
        patient.addPrescription('grimpex')
        # stage 3
        for treat_time in xrange(150):
            size_.append(patient.update())
        result.extend(size_)

    plt.figure()
    plt.plot(range(len(result)), result)
    plt.title("Trail 1")
    plt.show()

    # 2
    trail_times = [150]
    result = []
    for trail_time in trail_times:
        viruses = []
        for i in range(100):
            resist_virus = ResistantVirus(maxBirthProb, clearProb, resitances, mutProb)
            viruses.append(resist_virus)

        patient = Patient(viruses, maxPop)

        size_ = []
        # stage 1
        for gen in xrange(150):
            size_.append(patient.update())
        patient.addPrescription('guttagonol')
        patient.addPrescription('grimpex')
        # stage 2
        for treat_time in xrange(150):
            size_.append(patient.update())
        result.extend(size_)

    plt.figure()
    plt.plot(range(len(result)), result)
    plt.title("Trail 2")
    plt.show()

problem7()

