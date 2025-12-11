import bird
import random
import math
import species
import operator

class Population:
    def __init__(self, size):
        self.birds = [bird.Bird(100, random.randint(50, 570)) for _ in range(size)]

        self.generation = 1
        self.species = []

        self.size = size

        # Random colors
        for b in self.birds:
            b.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def update_live_birds(self, ground, pipes, window):
        for b in self.birds:
            if b.alive:
                b.look(pipes, window)
                b.think()
                b.draw(window)
                b.update(ground, pipes)
    
    def natural_selection(self):
        print("SPECIATION")
        self.speciate()

        print("CALCULATING FITNESS")
        self.calculate_fitness()

        print("SORT BY FITNESS")
        self.sort_species_by_fitness()

        print("CHILDREN FOR NEXT GENERATION")
        self.next_generation()
    
    def speciate(self):
        for s in self.species:
            s.players = []
        
        for b in self.birds:
            add_to_species = False
            for s in self.species:
                if s.similarity(b.brain):
                    s.add_to_species(b)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(b))
    
    def calculate_fitness(self):
        for b in self.birds:
            b.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()
    
    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()
        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)
    
    def next_generation(self):
        children = []

        for s in self.species:
            children.append(s.champion.clone())
        
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))

        for s in self.species:
            for i in range(children_per_species):
                children.append(s.offspring())
        
        while len(children) < self.size:
            children.append(self.species[0].offspring())
        
        self.birds = children
        self.generation += 1

    def extinct(self):
        return all(not b.alive for b in self.birds)
