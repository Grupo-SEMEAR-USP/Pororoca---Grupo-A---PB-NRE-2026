"""Text metrics and confidence analysis."""

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def print_metrics(test_loss, labels, predictions):
    accuracy = accuracy_score(labels, predictions)
    precision = precision_score(labels, predictions, average="macro", zero_division=0)
    recall = recall_score(labels, predictions, average="macro", zero_division=0)
    f1 = f1_score(labels, predictions, average="macro", zero_division=0)

    print()
    print("     ==== ==== ====   TEST RESULTS   ==== ==== ====")
    print()
    print(f"Loss:      {test_loss:.4f}")
    print(f"Accuracy:  {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall:    {recall:.2%}")
    print(f"Macro F1:  {f1:.2%}")


def print_top_confusions(labels, predictions, class_names, top_k: int = 10):
    matrix = confusion_matrix(labels, predictions)
    confusions = []

    for true_class in range(matrix.shape[0]):
        for predicted_class in range(matrix.shape[1]):
            if true_class == predicted_class:
                continue
            count = matrix[true_class, predicted_class]
            if count > 0:
                confusions.append((count, true_class, predicted_class))

    confusions.sort(reverse=True)
    print()
    print(f"     ==== ==== ====   Top {top_k} Confusions   ==== ==== ====")
    print()

    for count, true_class, predicted_class in confusions[:top_k]:
        print(
            f"Classe        {class_names[true_class]:25s} "
            f"→ Classe      {class_names[predicted_class]:25s}: "
            f"{count} vezes"
        )


def get_classification_report(labels, predictions, class_names):
    return classification_report(
        labels,
        predictions,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )


def analyze_confidence(labels, predictions, confidences):
    correct_confidences = []
    wrong_confidences = []

    for label, prediction, confidence in zip(labels, predictions, confidences):
        target = correct_confidences if label == prediction else wrong_confidences
        target.append(confidence)

    avg_correct = (
        sum(correct_confidences) / len(correct_confidences)
        if correct_confidences
        else None
    )
    avg_wrong = (
        sum(wrong_confidences) / len(wrong_confidences)
        if wrong_confidences
        else None
    )
    wrong_90 = sum(confidence >= 0.90 for confidence in wrong_confidences)
    wrong_95 = sum(confidence >= 0.95 for confidence in wrong_confidences)

    print()
    print("     ==== ==== ====   CONFIDENCE ANALYSIS   ==== ==== ====")
    print()
    print(
        "Avg confidence when correct: "
        + (f"{avg_correct:.2%}" if avg_correct is not None else "N/A")
    )
    print(
        "Avg confidence when wrong:   "
        + (f"{avg_wrong:.2%}" if avg_wrong is not None else "N/A")
    )
    print(f"Wrong predictions >= 90%: {wrong_90}")
    print(f"Wrong predictions >= 95%: {wrong_95}")


def print_high_confidence_errors(errors, class_names, top_k: int = 15):
    sorted_errors = sorted(
        errors,
        key=lambda item: item["confidence"],
        reverse=True,
    )
    print()
    print(
        "     ==== ==== ====   "
        f"Top {top_k} High Confidence Errors   ==== ==== ===="
    )
    print()

    for error in sorted_errors[:top_k]:
        true_name = class_names[error["true"]]
        predicted_name = class_names[error["predicted"]]
        print(
            f"{true_name:25s} → {predicted_name:25s} | "
            f"{error['confidence']:.2%}"
        )


def _class_results(report, class_names):
    return [
        (
            report[class_name]["f1-score"],
            report[class_name]["precision"],
            report[class_name]["recall"],
            int(report[class_name]["support"]),
            class_name,
        )
        for class_name in class_names
    ]


def _print_ranked_classes(title, results, top_k):
    print()
    print(f"     ==== ==== ====   {title} {top_k} Classes   ==== ==== ====")
    print()
    for f1, precision, recall, support, class_name in results[:top_k]:
        print(
            f"{class_name:25s} | "
            f"P: {precision:6.2%} | "
            f"R: {recall:6.2%} | "
            f"F1: {f1:6.2%} | "
            f"N: {support} |"
        )
    print()


def print_best_classes(report, class_names, top_k: int = 10):
    results = sorted(_class_results(report, class_names), reverse=True)
    _print_ranked_classes("Best", results, top_k)


def print_worst_classes(report, class_names, top_k: int = 10):
    results = sorted(_class_results(report, class_names))
    _print_ranked_classes("Worst", results, top_k)
