#!/usr/bin/env python
# encoding: utf-8

# 6.00 Problem Set 12
#
# Name: Scott Brenner
# Collaborators: http://curiousreef.com/class/mit-opencourseware-600-introduction/lesson/23/assgn/1/
# Time: Too long.

import numpy
import random
import pylab


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
        # TODO
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
        # TODO
        if random.random() <= self.clearProb:
            return True
        else:
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
        # TODO
        if random.random() <= (self.maxBirthProb * (1 - popDensity)):
            # print "virus reproduces"
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException('In reproduce()')


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
        # TODO
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):
        """
        Gets the current total virus population.
        returns: The total virus population (an integer)
        """
        # TODO
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
        # TODO
        # Determine whether each virus particle survives and updates the
        # list of virus particles accordingly.
        newViruses = []
        for index, virus in reversed(list(enumerate(self.viruses))):
            if virus.doesClear():
                # print "Virus clears"
                # pop virus from viruses list
                self.viruses.pop(index)
            else:
                popDensity = self.getTotalPop() / float(self.maxPop)
                try:
                    # determine if surving virus reproduces
                    # append any offspring to new virus list
                    newViruses.append(virus.reproduce(popDensity))
                except NoChildException:
                    continue
        # print "self.viruses =", self.viruses
        # print "newViruses =",  newViruses
        # add the new viruses to the list of patient viruses
        self.viruses = self.viruses + newViruses
        # print self.viruses

        return self.getTotalPop()


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
    # TODO
    # Create 100 viruses with
    #	maxBirthProb = 0.1
    #	clearProb = 0.05
    listOfViruses = []
    print "\ncreating virues...",
    for each in range(100):
        listOfViruses.append(SimpleVirus(0.1, .05))
        print each,

    # Create a patient with 100 viruses and maxPop of 1000
    print "\nCreating patient"
    testPatient = SimplePatient(listOfViruses, 1000)

    # Run the 300 step times on patient.  Record the virus population after each step.  The initial population is 100.
    listOfVirusPop = []
    timeSteps = []
    print "\nRunning time step",
    for each in range(300):
        print each,
        listOfVirusPop.append(testPatient.update())
        timeSteps.append(each)

    # graph results
    pylab.figure()
    pylab.plot(timeSteps, listOfVirusPop)
    pylab.ylabel('Viruse Population')
    pylab.xlabel('Timesteps')
    pylab.title('ps12.py - Problem 2: Total virus population over time')


# pylab.show()


# problem2()


# Writeup:  Somewhere between 100 and 150 steps the virus population stops growing, stabilizing around 475 (fluctuating between 450 & 500).


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
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
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
        # TODO
        # lookup drug in the self.resistances dictionary
        # if the value is true return true, else return false.
        return self.resistances.get(drug, False)

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
        # TODO
        # 	The instructions are unclear on whether offspring viruses inherit
        #	the same mutProb as their partent?	I assumed that they do.

        for drug in activeDrugs:
            if not self.getResistance(drug):
                raise NoChildException()
        # If we get here then we know the virus is resistent to all of the activeDrugs

        # Now let's see if it reproduces
        if random.random() <= (self.maxBirthProb * (1 - popDensity)):
            # figure out the resistances, mutProb
            newResistances = {}
            for drug in self.resistances:
                if random.random() <= (1 - self.mutProb):
                    newResistances[drug] = self.resistances[drug]
                else:
                    newResistances[drug] = not self.resistances[drug]
            return ResistantVirus(self.maxBirthProb, self.clearProb, newResistances, self.mutProb)
        else:
            raise NoChildException()


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
        # TODO
        self.viruses = viruses
        self.maxPop = maxPop
        self.presecribedDrugs = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        self.presecribedDrugs.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        # TODO
        return self.presecribedDrugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.
        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])
        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        resistantPopulation = 0
        for virus in self.viruses:
            drugsResisted = 0
            for drug in drugResist:  # drugResist is a list of drugs
                if virus.getResistance(drug):
                    drugsResisted += 1
            if drugsResisted == len(drugResist):
                resistantPopulation += 1
        return resistantPopulation

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
        # TODO
        newViruses = []
        for index, virus in reversed(list(enumerate(self.viruses))):
            if virus.doesClear():
                self.viruses.pop(index)
            else:
                popDensity = self.getTotalPop() / float(self.maxPop)
                try:
                    newViruses.append(virus.reproduce(popDensity, self.presecribedDrugs))
                except NoChildException:
                    continue
        self.viruses = self.viruses + newViruses
        return self.getTotalPop()


#
# PROBLEM 4
#
def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    Total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    simulationSteps = 300
    #	Patient variables.
    initialViruseCount = 100
    maxPop = 1000
    # Virus variables:
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False}
    mutProb = 0.005

    #	Create viruses
    listOfViruses = []
    print "\nCreating viruses...",
    for each in range(initialViruseCount):
        listOfViruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    # Create a patient with 100 viruses and maxPop of 1000
    print "\nCreating patient"
    testPatient = Patient(listOfViruses, maxPop)

    # Run 300 timestep on patient.  Record the virus population after each step.  The initial population is 100.  At the 150th timestep
    listOfVirusPop = []
    guttagonolResistant = []
    for each in range(simulationSteps):
        listOfVirusPop.append(testPatient.update())
        guttagonolResistant.append(testPatient.getResistPop(['guttagonol']))
        if each == 150: testPatient.addPrescription("guttagonol")

    # graph results
    pylab.figure()
    pylab.plot(listOfVirusPop, label='Total')
    pylab.plot(guttagonolResistant, label='Guttagonol-resistant viruses')
    pylab.ylabel('Viruse Population')
    pylab.xlabel('Timesteps')
    pylab.title('Problem 4: Total virus population over time. Guttagonol prescribed at 150.')
    pylab.legend(loc=2)
    pylab.show()


problem4()


# As in the other simulations the virus population stabilizes after 150 time steps at about 450-500 viruses. Then number of Guttagonol resistant viruses is negligible until Guttagonol is introduced.  After Guttagonol is introduced, the virus population plummets until a sufficient number develop resistance to Guttagonol, the the virus population appears to return to 450.
# The trends were consistent with my intuition, but I was surprised that the virus population, after the introduction of Guttagonol, return to 450-500.  I thought it would recover, but stabilize at a lower population.  I figured that since some of the descendants of each virus would mutate to lose their resistance to Guttagonol only a smaller population could be sustained.


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

    If the virus population is less than 50, the patient is considered cured or in remission.
    """
    # TODO
    numPatients = 200

    # ==================================================================
    # = Run simulation for 300 steps, then treat, then 150 more steps. =
    # ==================================================================
    title = "ps12.py - Problem 5: " + str(numPatients) + " patients-- 300 timesteps, Treat, 150 more timesteps."
    print
    print title
    virusCounts = []
    numCured = 0
    for each in range(numPatients):
        finalViruses = runPatietTreatment(450, 300, "guttagonol")
        # print "\nPatient", each, finalViruses,
        virusCounts.append(finalViruses)
        if finalViruses <= 50:
            numCured += 1
    print "\nOf the %i patients in the trial, %i were cured ( %3.1f%% ).  %3.1f%% were not cured." % (
    numPatients, numCured, 100 * (float(numCured) / float(numPatients)),
    100 * (1 - float(numCured) / float(numPatients)))

    # graph results
    pylab.figure()
    pylab.hist(virusCounts)
    pylab.ylabel('Number of Patients')
    pylab.xlabel('Final Total Virus Populations --' + str(100 * (float(numCured) / float(numPatients))) + "% cured.")
    pylab.title(title)

    # ==================================================================
    # = Run simulation for 150 steps, then treat, then 150 more steps. =
    # ==================================================================
    title = "Problem 5:" + str(numPatients) + " patients-- 150 timesteps, Treat, 150 more timesteps."
    print
    print title
    virusCounts = []
    numCured = 0
    for each in range(numPatients):
        finalViruses = runPatietTreatment(300, 150, "guttagonol")
        # print "\nPatient", each, finalViruses,
        virusCounts.append(finalViruses)
        if finalViruses <= 50:
            numCured += 1
    print "\nOf the %i patients in the trial, %i were cured ( %3.1f%% ).  %3.1f%% were not cured." % (
    numPatients, numCured, 100 * (float(numCured) / float(numPatients)),
    100 * (1 - float(numCured) / float(numPatients)))

    # graph results
    pylab.figure()
    pylab.hist(virusCounts)
    pylab.ylabel('Number of Patients')
    pylab.xlabel('Final Total Virus Populations --' + str(100 * (float(numCured) / float(numPatients))) + "% cured.")
    pylab.title(title)

    # ==================================================================
    # = Run simulation for 75 steps, then treat, then 150 more steps. =
    # ==================================================================
    title = "Problem 5:" + str(numPatients) + " patients--  75 timesteps, Treat, 150 more timesteps."
    print
    print title
    virusCounts = []
    numCured = 0
    for each in range(numPatients):
        finalViruses = runPatietTreatment(225, 75, "guttagonol")
        # print "\nPatient", each, finalViruses,
        virusCounts.append(finalViruses)
        if finalViruses <= 50:
            numCured += 1
    print "\nOf the %i patients in the trial, %i were cured ( %3.1f%% ).  %3.1f%% were not cured." % (
    numPatients, numCured, 100 * (float(numCured) / float(numPatients)),
    100 * (1 - float(numCured) / float(numPatients)))

    # graph results
    pylab.figure()
    pylab.hist(virusCounts)
    pylab.ylabel('Number of Patients')
    pylab.xlabel('Final Total Virus Populations --' + str(100 * (float(numCured) / float(numPatients))) + "% cured.")
    pylab.title(title)

    # ==================================================================
    # = Run simulation for 0 steps, then treat, then 150 more steps. =
    # ==================================================================
    title = "Problem 5:" + str(numPatients) + " patients--0 timesteps, treat, 75 more timesteps."
    print
    print title
    virusCounts = []
    numCured = 0
    for each in range(numPatients):
        finalViruses = runPatietTreatment(75, 0, "guttagonol")
        # print "\nPatient", each, finalViruses,
        virusCounts.append(finalViruses)
        if finalViruses <= 50:
            numCured += 1
    print "\nOf the %i patients in the trial, %i were cured ( %3.1f%% ).  %3.1f%% were not cured." % (
    numPatients, numCured, 100 * (float(numCured) / float(numPatients)),
    100 * (1 - float(numCured) / float(numPatients)))

    # graph results
    pylab.figure()
    pylab.hist(virusCounts)
    pylab.ylabel('Number of Patients')
    pylab.xlabel('Final Total Virus Populations --' + str(100 * (float(numCured) / float(numPatients))) + "% cured.")
    pylab.title(title)
    pylab.show()


def runPatietTreatment(simulationSteps, timeTillTreatment, drug, initialViruseCount=100, maxPop=1000, maxBirthProb=0.1,
                       clearProb=0.05, mutProb=0.005, resistances={'guttagonol': False}):
    """
    This helper function takes the above parametrs and returns
    the virus populaton at the end of the treatment.
    """
    # Create Patient
    virusCount = 0
    listOfViruses = []
    for each in range(initialViruseCount):
        listOfViruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
    testPatient = Patient(listOfViruses, maxPop)

    for each in range(simulationSteps):
        virusCount = testPatient.update()
        if each == timeTillTreatment: testPatient.addPrescription(drug)
    return virusCount


# problem5()


# Writeup:
# I repeated each condition 200 times.  This was more that enough to obtain a reasonable distribution.  I can tell the distribution is reasonable because the number of trial in each “bucket” of the histogram is above.  In addition, the outcome matched my understanding of reality--the longer treatment is delayed, the less likely it is to be successful.
#
# This relationship arises in the model because the longer treatment delay, the more time the viruses have to mutate Guttagonol resistance.  If the drug is administered right at the start there are few viruses, and none are resistant.  The more time the elapses, the larger the virus population and the larger the population of Guttagonol-resistant viruses
#
# When treatment is delayed until after 300 timesteps only  2.5% of the patients are cured or in remission.97.5% are not cured.
#
# When treatment is delayed until after 150 timesteps only  5% of the patients are cured or in remission.95% are not cured.
#
# When treatment is delayed until after 75 timesteps only 16% of the patients are cured or in remission.84% are not cured.
#
# When treatment is not delayed 99.5% of the patients are cured or in remission. .54% are not cured.
# Delay 			% Cured
# 300				2.5%
# 150				5%
# 75				16%
# 0					99.5%

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

    viruses = 100
    maxPop = 1000

    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {‘guttagonol’:False ‘grimpex’:False}
    mutProb = 0.005

    Run the simulation for 150 time steps before administering guttagonol to the patient. Then run the simulation for 300, 150, 75, and 0 time steps before administering a second drug, grimpex, to the patient. Finally, run the simulation for an additional 150 time steps.


    """
    # Initial Values
    patientsPerScheme = 30
    treatmentSchemes = [300, 150, 75, 0]
    initialViruseCount = 100
    maxPop = 1000
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False, 'grimpex': False}
    mutProb = 0.005

    # Create a list of virusus
    listOfViruses = []
    for each in range(initialViruseCount):
        listOfViruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    for timeTillTreatment in treatmentSchemes:
        finalVirusCounts = []
        numCured = 0
        for patient in range(patientsPerScheme):
            testPatient = Patient(listOfViruses, maxPop)
            continueTrial = True
            stepCount = 1
            while stepCount < timeTillTreatment + 301:
                virusCount = testPatient.update()
                stepCount += 1
                if stepCount == 150:
                    testPatient.addPrescription("guttagonol")
                if stepCount == timeTillTreatment + 150:
                    testPatient.addPrescription("grimpex")
            finalVirusCounts.append(virusCount)
            if virusCount <= 50:
                numCured += 1

        print "These are the final virus counts after running 150 steps, treating with Guttagonol, running %i more steps, adding Grimpex, then running 150 more steps:" % timeTillTreatment
        print finalVirusCounts
        print "\nOf the %i patients in the scheme, %i were cured ( %3.1f%% ).  %3.1f%% were not cured." % (
        patientsPerScheme, numCured, 100 * (float(numCured) / float(patientsPerScheme)),
        100 * (1 - float(numCured) / float(patientsPerScheme)))
        title = "ps12.py - Problem 6: %i steps till treatment with 2nd drug. Cure rate = %2.0f%%." % (
        timeTillTreatment, 100 * (float(numCured) / float(patientsPerScheme)))
        # graph results
        pylab.figure()
        pylab.hist(finalVirusCounts)
        pylab.ylabel('Number of Patients')
        pylab.xlabel('Final Total Virus Populations')
        pylab.title(title)
    pylab.show()


# problem6()


# Write up:
# As with the earlier experiments, delaying treatment reduces the likelihood that the treatment will eradicate the viruses.  The more time the viruses are given to build their population and evolved resistance to a drug the more likely the drug will fail.
#
# However, in this dual drug treatment is more effective than a single drug treatment, even when the second drug is delayed.  This is likely because the first drug had reduced the population of the viruses.

# Delay 		% Cured
# 300			~7%
# 150			~10%
# 75			~93%
# 0				~100%

#
# PROBLEM 7
#
def problem7(guttagonolAt, grimpexAt):
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.
    """
    # TODO
    # Initial Values
    initialViruseCount = 100
    maxPop = 1000
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False, 'grimpex': False}
    mutProb = 0.005
    totalViruses = []
    guttagonolResistant = []
    grimpexResistant = []
    dualResistant = []
    stepCount = 1

    # Create a list of virusus
    listOfViruses = []
    for each in range(initialViruseCount):
        listOfViruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    # Create Patient
    testPatient = Patient(listOfViruses, maxPop)

    # this while loop asumes that grimpex is adminstered last and the 300 more time steps are simulated.
    while stepCount < grimpexAt + 301:
        virusCount = testPatient.update()
        stepCount += 1
        if stepCount == guttagonolAt:
            testPatient.addPrescription("guttagonol")
        if stepCount == grimpexAt:
            testPatient.addPrescription("grimpex")
        totalViruses.append(testPatient.getTotalPop())
        guttagonolResistant.append(testPatient.getResistPop(['guttagonol']))
        grimpexResistant.append(testPatient.getResistPop(['grimpex']))
        dualResistant.append(testPatient.getResistPop(['guttagonol', 'grimpex']))
    # graph results
    title = "ps12.py - Problem 7: Guttagonol @%i; Grimpex@ %i." % (guttagonolAt, grimpexAt)

    pylab.figure()
    pylab.plot(totalViruses, label='Total')
    pylab.plot(guttagonolResistant, label='Guttagonol-resistant virus')
    pylab.plot(grimpexResistant, label='Grimpex-resistant virus')
    pylab.plot(dualResistant, label='Resistant to both drugs')
    pylab.ylabel('Number Viruses')
    pylab.xlabel('Time')
    pylab.title(title)
    pylab.legend(loc=1)
    pylab.show()


# problem7(guttagonolAt=150, grimpexAt=300)
# problem7(guttagonolAt=150, grimpexAt=150)

# ====================
# = Problem 8 writup =
# ====================
# To model patients forgetting to take their drugs I would add a property to the patient object and modify the getPrescriptions() method.
#
# The property, a float, would model the likelihood that a patient would take their prescriptions, e.g., .9 for a patient who takes their prescriptions 90% of the time.
#
# The getPrescriptions() method would be modified to model this likelihood.  For example if the likelihood the patient would take their drugs is .9 then the method would return the active drugs only 90% of the time.