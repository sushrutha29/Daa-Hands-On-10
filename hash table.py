#include <stdio.h>
#include <stdlib.h>
#define INITIAL_SIZE 10
#define GROWTH_FACTOR 2
#define SHRINK_FACTOR 2
#define LOAD_FACTOR_THRESHOLD 0.75
#define SHRINK_THRESHOLD 0.25


typedef struct Node 
{
    int key;
    int data;
    struct Node* next;
    struct Node* prev;
} Node;


typedef struct 
{
    int n;
    int count;
    Node** arr;
} HashTable;


Node* createNode(int key, int data) 
{
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->key = key;
    newNode->data = data;
    newNode->next = NULL;
    newNode->prev = NULL;
    return newNode;
}


HashTable* createTable() 
{
    HashTable* h = (HashTable*)malloc(sizeof(HashTable));
    h->n = INITIAL_SIZE;
    h->count = 0;
    h->arr = (Node**)malloc(sizeof(Node*) * h->n);
    for (int i = 0; i < h->n; i++) {
        h->arr[i] = NULL;
    }
    return h;
}


int hash(int key, int n) 
{
    const double A = 0.52625283; 
    double val = key * A;
    val -= (int)val;
    return (int)(n * val);
}


void insert(HashTable* h, int key, int data) 
{
    int index = hash(key, h->n);
    Node* newNode = createNode(key, data);
    if (h->arr[index] == NULL) 
    {
        h->arr[index] = newNode;
    } else {
        newNode->next = h->arr[index];
        h->arr[index]->prev = newNode;
        h->arr[index] = newNode;
    }
    h->count++;

    
    if ((double)h->count / h->n > LOAD_FACTOR_THRESHOLD) 
    {
        
        int newSize = h->n * GROWTH_FACTOR;
        Node** newTable = (Node**)malloc(sizeof(Node*) * newSize);
        for (int i = 0; i < newSize; i++)
        {
            newTable[i] = NULL;
        }

        for (int i = 0; i < h->n; i++) 
        {
            Node* current = h->arr[i];
            while (current != NULL) 
            {
                Node* next = current->next;
                int newIndex = hash(current->key, newSize);
                if (newTable[newIndex] == NULL) 
                {
                    newTable[newIndex] = current;
                    current->next = NULL;
                    current->prev = NULL;
                } else
                {
                    current->next = newTable[newIndex];
                    newTable[newIndex]->prev = current;
                    newTable[newIndex] = current;
                }
                current = next;
            }
        }

        free(h->arr);
        h->arr = newTable;
        h->n = newSize;
    }
}


int get(HashTable* h, int key) 
{
    int index = hash(key, h->n);
    Node* current = h->arr[index];
    while (current != NULL) 
    {
        if (current->key == key)
        {
            return current->data;
        }
        current = current->next;
    }
    return -1; 
}


void delete(HashTable* h, int key) 
{
    int index = hash(key, h->n);
    Node* current = h->arr[index];
    while (current != NULL) 
    {
        if (current->key == key) 
        {
            if (current->prev != NULL)
                current->prev->next = current->next;
            if (current->next != NULL)
                current->next->prev = current->prev;
            if (h->arr[index] == current)
                h->arr[index] = current->next;
            free(current);
            h->count--;

            
            if ((double)h->count / h->n < SHRINK_THRESHOLD && h->n > INITIAL_SIZE) 
            {
                
                int newSize = h->n / SHRINK_FACTOR;
                Node** newTable = (Node**)malloc(sizeof(Node*) * newSize);
                for (int i = 0; i < newSize; i++) {
                    newTable[i] = NULL;
                }

                for (int i = 0; i < h->n; i++) 
                {
                    Node* current = h->arr[i];
                    while (current != NULL) 
                    {
                        Node* next = current->next;
                        int newIndex = hash(current->key, newSize);
                        if (newTable[newIndex] == NULL) 
                        {
                            newTable[newIndex] = current;
                            current->next = NULL;
                            current->prev = NULL;
                        } else
                        {
                            current->next = newTable[newIndex];
                            newTable[newIndex]->prev = current;
                            newTable[newIndex] = current;
                        }
                        current = next;
                    }
                }

                free(h->arr);
                h->arr = newTable;
                h->n = newSize;
            }

            return;
        }
        current = current->next;
    }
}


void print(HashTable* h) 
{
    for (int i = 0; i < h->n; i++)
    {
        printf("[%d]: ", i);
        Node* current = h->arr[i];
        while (current != NULL)
        {
            printf("(%d, %d) ", current->key, current->data);
            current = current->next;
        }
        printf("\n");
    }
}


void freeTable(HashTable* h) 
{
    for (int i = 0; i < h->n; i++) 
    {
        Node* current = h->arr[i];
        while (current != NULL)
        {
            Node* temp = current;
            current = current->next;
            free(temp);
        }
    }
    free(h->arr);
    free(h);
}

int main()
{
    HashTable* h = createTable();

    insert(h, 1, 21);
    insert(h, 2, 22);
    insert(h, 3, 23);
    insert(h, 4, 24);
    insert(h, 5, 25);

    printf("HashTable after inserting:\n");
    print(h);

    printf("\nValue for key 4: %d\n", get(h, 4));

    delete(h, 4);

    printf("\nHashTable after deleting key 4:\n");
    print(h);

    freeTable(h);
    return 0;
}

"""
output:
HashTable after inserting:
[0]: (2, 22) 
[1]: (4, 24) 
[2]: 
[3]: 
[4]: 
[5]: (3, 23) (1, 21) 
[6]: (5, 25) 
[7]: 
[8]: 
[9]: 

Value for key 4: 24

HashTable after deleting key 4:
[0]: (2, 22) 
[1]: 
[2]: 
[3]: 
[4]: 
[5]: (3, 23) (1, 21) 
[6]: (5, 25) 
[7]: 
[8]: 
[9]: 

"""
