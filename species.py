import operator
import random

class Species:
    def __init__(self, bird) -> None:
        self.birds = [bird]
        self.average_fitness = 0
        self.treshold = 1.2
        self.benchmark_fitness = bird.fitness
        self.benchmark_brain = bird.brain.clone()
        self.champion = bird.clone()
    
    def similarity(self, brain) -> bool:
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.treshold > similarity

    @staticmethod
    def weight_difference(brain1, brain2) -> float:
        total_weight_difference = 0
        for i in range(len(brain1.connections)):
            for j in range(len(brain2.connections)):
                if i == j:
                    total_weight_difference += abs(brain1.connections[i].weight - brain2.connections[j].weight)
        return total_weight_difference
    
    def add_to_species(self, bird) -> None:
        self.birds.append(bird)

    def sort_players_by_fitness(self) -> None:
        self.birds.sort(key=operator.attrgetter('fitness'), reverse=True)
        if self.birds[0].fitness > self.benchmark_fitness:
            self.benchmark_fitness = self.birds[0].fitness
            self.champion = self.birds[0].clone()
    
    def calculate_average_fitness(self) -> None:
        total_fitness = 0
        for b in self.birds:
            total_fitness += b.fitness
        if self.birds:
            self.average_fitness = int(total_fitness / len(self.birds))
        else:
            self.average_fitness = 0
    
    def offspring(self):
        if len(self.birds) == 1:
            chick = self.birds[0].clone()
            chick.brain.mutate()
            return chick
        chick = self.birds[random.randint(1, len(self.birds)-1)].clone()
        chick.brain.mutate()
        return chick