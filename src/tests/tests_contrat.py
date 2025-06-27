"""
Phase 3 : Tests de contrat
3.1 Validation des schémas JSON
Définir et implémenter des schémas de validation pour : - Structure des réponses API avec propriétés requises et optionnelles - Types de données et formats (nombres, chaînes, dates) - Contraintes de validation (énumérations, plages de valeurs) - Gestion des propriétés imbriquées (température, conditions météo)

Exemple de schéma simplifié :

const weatherSchema = {
  type: 'object',
  required: ['city', 'temperature'],
  properties: {
    city: { type: 'string' },
    temperature: {
      type: 'object',
      required: ['current']
      // À compléter...
    }
  }
};
Faites le votre ici
3.2 Tests de contrat avec les APIs externes
Mock des réponses des APIs tierces
Tests de robustesse en cas de changement de format
Validation des transformations de données
"""