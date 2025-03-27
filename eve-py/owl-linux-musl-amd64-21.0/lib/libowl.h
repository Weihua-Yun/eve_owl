#ifndef __LIBOWL_H
#define __LIBOWL_H

#include <graal_isolate.h>


#if defined(__cplusplus)
extern "C" {
#endif

/*
 * Read a (deterministic) automaton from a char* serialised in the HOA format.
 * Decodes a 0 terminated C char* to a Java string using the platform's default charset.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * automaton_parse(graal_isolatethread_t*, char*);

/*
 * Translate the given formula to deterministic parity automaton.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * automaton_of(graal_isolatethread_t*, void *, ltl_to_dpa_translation_t);

/*
 * Translate the given formula to deterministic parity automaton.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * automaton_of0(graal_isolatethread_t*, void *, ltl_to_dpa_translation_t, int);

/*
 * Translate the given formula to deterministic parity automaton.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * automaton_of1(graal_isolatethread_t*, void *, ltl_to_dpa_translation_t, int, ltl_translation_option_t);

/*
 * Translate the given formula to deterministic parity automaton.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * automaton_of2(graal_isolatethread_t*, void *, ltl_to_dpa_translation_t, int, ltl_translation_option_t, ltl_translation_option_t);

/*
 * Translate the given formula to deterministic parity automaton.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * automaton_of3(graal_isolatethread_t*, void *, ltl_to_dpa_translation_t, int, ltl_translation_option_t, ltl_translation_option_t, ltl_translation_option_t);

/*
 * Translate the given formula to deterministic parity automaton.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * automaton_of4(graal_isolatethread_t*, void *, ltl_to_dpa_translation_t, int, ltl_translation_option_t, ltl_translation_option_t, ltl_translation_option_t, ltl_translation_option_t);

/*
 * Translate the given formula to deterministic parity automaton.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * automaton_of5(graal_isolatethread_t*, void *, ltl_to_dpa_translation_t, int, ltl_translation_option_t, ltl_translation_option_t, ltl_translation_option_t, ltl_translation_option_t, ltl_translation_option_t);

acceptance_t automaton_acceptance_condition(graal_isolatethread_t*, void *);

int automaton_acceptance_condition_sets(graal_isolatethread_t*, void *);

int automaton_atomic_propositions(graal_isolatethread_t*, void *);

/*
 * Atomic propositions of the range [0, s[ are uncontrollable and [s, l[ are controllable, where s is the value returned by this method. -1 is the default return value, when this value cannot be determined.
 */
int automaton_atomic_propositions_uncontrollable_size(graal_isolatethread_t*, void *);

size_t automaton_atomic_propositions_label(graal_isolatethread_t*, void *, int, char*, size_t);

/*
 * Serialise the edges leaving the given state into a tree buffer, edge buffer, and an 
 * optional score buffer. If the scores are not required, the pointer may be set to NULL.
 * The pointer returned via the vector_{int,double}_t structures must be freed using
 * the method `free_unmanaged_memory`.
 */
void automaton_edge_tree(graal_isolatethread_t*, void *, int, vector_int_t*, vector_int_t*, vector_double_t*);

/*
 * Returns a feature vector of the same length as the passed state vector. The memory is 
 * managed by Java and at the moment there is no API-call to deallocate it.
 */
zielonka_normal_form_state_t* automaton_extract_features_normal_form_zielonka_construction(graal_isolatethread_t*, void *, vector_int_t*);

/*
 * Signature: 
 * boolean (void* automaton, vector_int_t* states, vector_int_t* features)
 * Extract features from the given set of states of an automaton. This method returns `true` if the features disambiguate the given state set. If `false` is returned, the caller of the method needs to disambiguate two states with the same set of features by additional means, e.g. by adding extra bits. The caller might request the inclusion of the accepting and rejecting sink by adding OWL_ACCEPTING_SINK and OWL_REJECTING_SINK to the state set. These states are then added on a best-effort basis. [Some automata do not have a canonical accepting and rejecting sinks]
 * The encoding of the feature vector is as follows:
 * 
 * |---------------------------------------------------------------------------------------------------------------------|
 * | int (state) | feature_type_t | ... | OWL_FEATURE_SEPARATOR | feature_type | ... | OWL_SEPARATOR | int (state) | ... |
 * |---------------------------------------------------------------------------------------------------------------------|
 * 
 * Features are then encoded as follows.
 * - PERMUTATION: an int sequence of variable length with no duplicates.
 * - ROUND_ROBIN_COUNTER: a single int.
 * - TEMPORAL_OPERATORS_PROFILE: an int sequence of variable length with no duplicates.
 */
int automaton_extract_features(graal_isolatethread_t*, void *, vector_int_t*, vector_int_t*);

void destroy_object_handle(graal_isolatethread_t*, void *);

void free_unmanaged_memory(graal_isolatethread_t*, void *);

size_t print_object_handle(graal_isolatethread_t*, void *, char*, size_t);

size_t owl_version(graal_isolatethread_t*, char*, size_t);

/*
 * Parse the given string with the given atomic propositions and return an LTL formula.
 * Decodes a 0 terminated C char* to a Java string using the platform's default charset.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * ltl_formula_parse(graal_isolatethread_t*, char*, char**, int);

/*
 * Parse the given string with the given atomic propositions and return an LTL formula with finite semantics.
 * Decodes a 0 terminated C char* to a Java string using the platform's default charset.
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * ltl_formula_parse_with_finite_semantics(graal_isolatethread_t*, char*, char**, int);

/*
 * Simplify the given LTL formula assuming a Game-semantics where atomic propositions less 
 * than `firstOutputAtomicProposition` is controlled by the environment trying to dissatisfy 
 * the formula and atomic proposition greater or equal are controlled by the system. The 
 * status of atomic proposition is written to the passed int pointer using the encoding 
 * provided by `atomic_proposition_status_t`
 * This function returns a void pointer to an opaque Java object handle. The object is not collected by the garbage collected unless 'destroy_object_handle' is called on the pointer.
 */
void * ltl_formula_simplify(graal_isolatethread_t*, void *, int, int*, int);

int run_main(int argc, char** argv);

void vmLocatorSymbol(graal_isolatethread_t* thread);

#if defined(__cplusplus)
}
#endif
#endif
