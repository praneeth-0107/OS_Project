#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
#include <time.h>

#define NUM_STUDENTS 10
#define CHAIRS 3

sem_t students;        
sem_t ta_sem;         
pthread_mutex_t mutex;

int waiting = 0;      
int all_done = 0;     

void help_student(int id) {
    printf("TA is helping student %d\n", id);
    sleep(rand() % 3 + 1); 
    printf("TA finished helping student %d\n", id);
}

void *ta_thread(void *arg) {
    while (1) {
        sem_wait(&students);
        pthread_mutex_lock(&mutex);

        if (all_done && waiting == 0) {
            pthread_mutex_unlock(&mutex);
            break;
        }

        waiting--;
        printf("TA calls a student. Waiting students left: %d\n", waiting);

        sem_post(&ta_sem);

        pthread_mutex_unlock(&mutex);

        sleep(rand() % 3 + 1);
    }

    printf("TA is done for the day.\n");
    return NULL;
}

void *student_thread(void *arg) {
    int id = *(int *)arg;
    free(arg);

    int helped = 0;

    while (!helped) {
        sleep(rand() % 5 + 1);

        pthread_mutex_lock(&mutex);

        if (waiting < CHAIRS) {
            waiting++;
            printf("Student %d sits in the hallway. Waiting: %d\n", id, waiting);

            sem_post(&students);

            pthread_mutex_unlock(&mutex);

            sem_wait(&ta_sem);

            printf("Student %d is getting help from TA.\n", id);
            help_student(id);
            helped = 1;
        } else {
            printf("No chair available. Student %d leaves and will come back later.\n", id);
            pthread_mutex_unlock(&mutex);
        }
    }

    printf("Student %d leaves after getting help.\n", id);
    return NULL;
}

int main() {
    srand(time(NULL));

    pthread_t ta;
    pthread_t students_threads[NUM_STUDENTS];

    pthread_mutex_init(&mutex, NULL);
    sem_init(&students, 0, 0); 
    sem_init(&ta_sem, 0, 0);  

    pthread_create(&ta, NULL, ta_thread, NULL);

    for (int i = 0; i < NUM_STUDENTS; i++) {
        int *id = malloc(sizeof(int));
        *id = i + 1;
        pthread_create(&students_threads[i], NULL, student_thread, id);
    }

    for (int i = 0; i < NUM_STUDENTS; i++) {
        pthread_join(students_threads[i], NULL);
    }

    pthread_mutex_lock(&mutex);
    all_done = 1;
    pthread_mutex_unlock(&mutex);

    sem_post(&students);

    pthread_join(ta, NULL);

    sem_destroy(&students);
    sem_destroy(&ta_sem);
    pthread_mutex_destroy(&mutex);

    return 0;
}
